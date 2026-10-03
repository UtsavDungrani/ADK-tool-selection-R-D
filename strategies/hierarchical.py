"""Two-stage selection: route to a namespace, then declare only its tools.

Stage 1  A cheap LLM call sees only the *domain* menu (~5-25 one-line
         descriptions) and names the relevant domain(s).
Stage 2  Every tool in the chosen domain(s) is declared, optionally narrowed
         to top-k by BM25 within the domain.

Why this is worth measuring separately from flat retrieval:

  - It degrades gracefully. Flat top-k retrieval that misses puts the right
    tool nowhere in the list. Domain routing that picks the right namespace
    guarantees the right tool is present, whatever the ranker does next.
  - The stage-1 prompt is short and *stable* across queries, so it is a good
    prefix-cache citizen -- the concern raised in adk-python#7241.
  - It is interpretable. When it fails you can see whether it routed wrong or
    ranked wrong. Flat retrieval gives you one undifferentiated number.

The honest cost: an extra LLM round trip before any tool is declared. That is
recorded in `last_cost` (real prompt/completion tokens from usage_metadata, not
an estimate) and the report adds it back. A strategy cannot look cheap by
hiding its own spend in a second model call.
"""

from __future__ import annotations

import os
import time

from catalog import DOMAIN_DESCRIPTIONS, ToolSpec

from .base import AuxCost, SelectionStrategy
from .lexical import BM25Strategy

_ROUTER_MODEL = "gemini-3.5-flash-lite"

_ROUTER_PROMPT = """You route a user request to the tool namespaces that could serve it.

Available namespaces:
{menu}

User request: {query}

Reply with ONLY a comma-separated list of namespace names from the list above,
most relevant first, at most {max_domains}. No explanation, no other text."""


class HierarchicalStrategy(SelectionStrategy):
    name = "hierarchical"
    description = "LLM routes to a namespace, then that namespace's tools are declared."

    def __init__(
        self,
        catalog: list[ToolSpec],
        model: str = _ROUTER_MODEL,
        max_domains: int = 2,
        rank_within_domain: bool = True,
    ):
        super().__init__(catalog)
        self.model = model
        self.max_domains = max_domains
        self.rank_within_domain = rank_within_domain
        self._client = None

        self.domains: dict[str, list[ToolSpec]] = {}
        for s in catalog:
            self.domains.setdefault(s.domain, []).append(s)

        self._menu = "\n".join(
            f"- {d}: {self._describe(d)}" for d in sorted(self.domains)
        )
        self._bm25: BM25Strategy | None = None

    @staticmethod
    def _describe(domain: str) -> str:
        if domain in DOMAIN_DESCRIPTIONS:
            return DOMAIN_DESCRIPTIONS[domain]
        # Filler domains have no hand-written blurb; a generic one keeps the
        # menu uniform rather than making filler conspicuously different (and
        # therefore conspicuously easy to reject).
        return f"Operations on {domain} records: create, update, search, list, export."

    def _get_client(self):
        if self._client is None:
            from google import genai

            api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
            if not api_key:
                raise RuntimeError(
                    "HierarchicalStrategy needs GOOGLE_API_KEY (or GEMINI_API_KEY) "
                    "for its stage-1 router call."
                )
            self._client = genai.Client(api_key=api_key)
        return self._client

    def warmup(self) -> None:
        if self.rank_within_domain:
            self._bm25 = BM25Strategy(self.catalog)
            self._bm25.warmup()

    def _route(self, query: str) -> tuple[list[str], AuxCost]:
        from google.genai import types

        t0 = time.perf_counter()
        prompt = _ROUTER_PROMPT.format(
            menu=self._menu, query=query, max_domains=self.max_domains
        )
        resp = self._get_client().models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.0,
                max_output_tokens=2048,
            ),
        )
        usage = getattr(resp, "usage_metadata", None)
        cost = AuxCost(
            llm_calls=1,
            prompt_tokens=getattr(usage, "prompt_token_count", 0) or 0,
            completion_tokens=getattr(usage, "candidates_token_count", 0) or 0,
            wall_ms=(time.perf_counter() - t0) * 1000.0,
        )

        text = (resp.text or "").strip()
        picked = []
        for raw in text.replace("\n", ",").split(","):
            d = raw.strip().strip("-* `").lower()
            if d in self.domains and d not in picked:
                picked.append(d)
        return picked[: self.max_domains], cost

    def select(self, query: str, k: int) -> list[ToolSpec]:
        picked, cost = self._route(query)
        self.last_cost = cost

        if not picked:
            # Router produced nothing usable. Falling back to the whole catalog
            # is deliberately the *expensive* failure: a silent fallback to a
            # small guess would hide router failures inside the accuracy number.
            return list(self.catalog)

        candidates: list[ToolSpec] = []
        for d in picked:
            candidates.extend(self.domains[d])

        if not self.rank_within_domain or len(candidates) <= k:
            return candidates[:k] if k < len(candidates) else candidates

        if self._bm25 is None:
            self.warmup()
        allowed = {s.name for s in candidates}
        ranked = [s for s in self._bm25.select(query, len(self.catalog)) if s.name in allowed]
        return ranked[:k]
