"""Hybrid RAG multi-tool selection strategy.

Decomposes compound user requests into distinct sub-goals, vector-retrieves
relevant candidate tools for each sub-goal using dense embeddings, and keeps
only the candidates that score close to that sub-goal's best match.

ON THE CUTOFF BEING RELATIVE, NOT ABSOLUTE

This filtered on an absolute cosine floor (`min_similarity=0.55`) until a sweep
showed the floor never fired. Gemini embedding scores over this catalog sit in
a narrow band -- roughly 0.65 to 0.80 -- so every candidate cleared 0.55 and
the filter was decoration. Raising the floor does not fix it: by 0.70 recall
collapses, and the "keep top-1 anyway" rescue fires on 20-65% of sub-goals,
which turns the filter into "take exactly one tool" rather than into a filter.

A margin below each sub-goal's own top score adapts to that band. Measured over
12 multi-tool prompts and the 132 eval tasks, a 0.03 margin holds recall exactly
where no filtering at all puts it while declaring ~45% fewer tools:

    cutoff                 set A recall / declared    set B recall / declared
    none                     100.0%  /  8.7             97.7%  /  3.0
    absolute 0.55 (old)      100.0%  /  8.7             97.7%  /  3.0   inert
    absolute 0.67            100.0%  /  7.9             95.5%  /  2.5   costs recall
    relative 0.03            100.0%  /  4.8             97.7%  /  1.7
    relative 0.02             94.9%  /  4.0             96.2%  /  1.5   too tight

The top match always clears a relative margin, so the rescue branch below is now
a guard against an empty catalog rather than part of normal operation.
"""

from __future__ import annotations

import os
import time
from typing import Optional

from catalog import ToolSpec
from .base import AuxCost, SelectionStrategy
from .embedding import EmbeddingCache, _DEFAULT_MODEL, _cosine

_DECOMPOSER_MODEL = "gemini-3.5-flash-lite"

_DECOMPOSER_PROMPT = """You are a query decomposition router.
Break the user's request into the distinct, atomic action goals it asks for --
one sub-goal per operation that needs its own tool.

Rules:
- Emit one sub-goal per operation the request actually asks for. Never invent,
  merge, or drop an operation.
- Each sub-goal names ONE action. Never write a sub-goal containing "or": if two
  readings are possible, pick the one the request supports.
- Never introduce a verb the request did not use. "Share a file" is not "send a
  message"; "page someone" is not "email someone".
- Carry the system forward. When a later clause continues working on something
  named earlier, name that system again -- "upload the deck to Box, then share
  it" gives a second sub-goal about sharing a Box file, not sharing in general.
- Keep the system name whenever the request gives one. It is the strongest
  signal the retriever has.
- Return ONLY the sub-goals, one per line, with no numbering, bullets, prefixes,
  or markdown.
- If the request describes a single task, return just that one task.

Examples:
Request: "git pr request and share message of pr request to the slack dashboard and if it is acceted then take code from merged main branch and run ci cd test"
Sub-goals:
list pull requests on github
send message to slack
run ci cd test workflow on merged branch

Request: "Create a Jira issue, schedule meeting on Google Calendar, store file in Google Drive, and make Stripe payment"
Sub-goals:
create jira issue
schedule meeting on google calendar
upload file to google drive
create stripe payment

Request: "Upload the signed contract to Box, share it with the legal team, and archive the previous version"
Sub-goals:
upload file to box
share box file with legal team
archive previous file version in box

User request: {query}"""


class RAGMultiToolStrategy(SelectionStrategy):
    name = "rag_multi"
    description = (
        "Hybrid RAG: decomposes compound query into sub-goals, vector-retrieves "
        "per sub-goal, and keeps candidates within a margin of each one's best match."
    )

    def __init__(
        self,
        catalog: list[ToolSpec],
        embedding_model: str = _DEFAULT_MODEL,
        decomposer_model: str = _DECOMPOSER_MODEL,
        # Keep a candidate when it scores within this much of its sub-goal's
        # best match. Relative, not absolute -- see the module docstring for the
        # sweep that killed the absolute floor. 0.02 is too tight; 0.03 is the knee.
        max_score_gap: float = 0.03,
        # 3, not 2: measured over 12 multi-tool queries against the
        # 350-tool catalog, k=2 reaches 97.4% gold recall and k=3 reaches
        # 100%. k=4 and k=5 add nothing but 2-4 more declared tools per
        # turn. The right value moved when the catalog grew -- at 132
        # tools near-twins were rare, and 2 was enough.
        k_per_subgoal: int = 3,
        max_total: int = 10,
        cache: Optional[EmbeddingCache] = None,
        batch_size: int = 64,
    ):
        super().__init__(catalog)
        self.embedding_model = embedding_model
        self.decomposer_model = decomposer_model
        self.max_score_gap = max_score_gap
        self.k_per_subgoal = k_per_subgoal
        self.max_total = max_total
        self.cache = cache or EmbeddingCache()
        self.batch_size = batch_size

        self._doc_vecs: list[list[float]] = []
        self._client = None

    def _get_client(self):
        if self._client is None:
            from google import genai
            from pathlib import Path

            api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
            if not api_key:
                env_file = Path(__file__).resolve().parent.parent / ".env"
                if env_file.exists():
                    for line in env_file.read_text(encoding="utf-8").splitlines():
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, _, v = line.partition("=")
                            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
                api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

            if not api_key:
                raise RuntimeError(
                    "RAGMultiToolStrategy needs GOOGLE_API_KEY (or GEMINI_API_KEY)."
                )
            self._client = genai.Client(api_key=api_key)
        return self._client

    def _embed(self, texts: list[str], task_type: str) -> tuple[list[list[float]], int]:
        from google.genai import types

        out: list[list[float] | None] = [
            self.cache.get(self.embedding_model, task_type, t) for t in texts
        ]
        missing = [i for i, v in enumerate(out) if v is None]
        api_calls = 0

        for start in range(0, len(missing), self.batch_size):
            chunk_idx = missing[start : start + self.batch_size]
            chunk = [texts[i] for i in chunk_idx]
            resp = self._get_client().models.embed_content(
                model=self.embedding_model,
                contents=chunk,
                config=types.EmbedContentConfig(task_type=task_type),
            )
            api_calls += 1
            for i, emb in zip(chunk_idx, resp.embeddings):
                vec = list(emb.values)
                out[i] = vec
                self.cache.put(self.embedding_model, task_type, texts[i], vec)
            # Flush per batch, not once at the end. Warming a 350-tool catalog
            # is hundreds of embed requests and the free tier caps them per
            # minute, so a 429 part-way through is normal. Flushing here means
            # the next attempt resumes instead of starting over.
            self.cache.flush()

        if api_calls:
            self.cache.flush()
        return [v for v in out if v is not None], api_calls

    def warmup(self) -> None:
        doc_task = "RETRIEVAL_DOCUMENT"
        texts = [s.index_text() for s in self.catalog]
        self._doc_vecs, _ = self._embed(texts, doc_task)

    def _decompose(self, query: str) -> tuple[list[str], AuxCost]:
        """Decompose compound query into atomic sub-goals using a fast LLM."""
        t0 = time.perf_counter()
        cost = AuxCost()
        # If the query is very brief, skip LLM decomposition to save latency
        words = query.strip().split()
        if len(words) <= 4:
            return [query.strip()], cost

        prompt = _DECOMPOSER_PROMPT.format(query=query)
        try:
            from google.genai import types as genai_types

            client = self._get_client()
            resp = client.models.generate_content(
                model=self.decomposer_model,
                contents=prompt,
                # Deterministic: `get_tools` runs this once per model request,
                # so a drifting split would change the declared tool list
                # between steps of a single turn and void the prompt cache.
                config=genai_types.GenerateContentConfig(temperature=0.0),
            )
            cost.llm_calls = 1
            if resp.usage_metadata:
                cost.prompt_tokens = resp.usage_metadata.prompt_token_count or 0
                cost.completion_tokens = resp.usage_metadata.candidates_token_count or 0

            text = resp.text.strip() if resp.text else ""
            lines = [line.strip("- *•\t\r") for line in text.splitlines() if line.strip()]
            sub_goals = [l for l in lines if len(l) > 3][:15]
            if not sub_goals:
                sub_goals = [query.strip()]
        except Exception:
            sub_goals = [query.strip()]

        cost.wall_ms = (time.perf_counter() - t0) * 1000.0
        return sub_goals, cost

    def select(self, query: str, k: int = 5) -> list[ToolSpec]:
        t0 = time.perf_counter()
        if not self._doc_vecs:
            self.warmup()

        sub_goals, decomp_cost = self._decompose(query)
        q_task = "RETRIEVAL_QUERY"
        q_vecs, embed_calls = self._embed(sub_goals, q_task)

        selected_indices: list[int] = []
        seen_indices: set[int] = set()

        for qv in q_vecs:
            scored = [(_cosine(qv, dv), i) for i, dv in enumerate(self._doc_vecs)]
            scored.sort(key=lambda si: (-si[0], si[1]))

            if not scored:
                continue

            # Keep what scores close to this sub-goal's own best match, so the
            # cutoff moves with the query instead of assuming a fixed scale.
            # The top match always clears its own margin, so this never comes
            # back empty -- the old "rescue top-1" branch is gone with the floor.
            cutoff = scored[0][0] - self.max_score_gap
            qualifying = [idx for score, idx in scored if score >= cutoff]

            for idx in qualifying[: self.k_per_subgoal]:
                if idx not in seen_indices:
                    seen_indices.add(idx)
                    selected_indices.append(idx)

        total_cost = AuxCost(
            llm_calls=decomp_cost.llm_calls,
            prompt_tokens=decomp_cost.prompt_tokens,
            completion_tokens=decomp_cost.completion_tokens,
            embed_calls=embed_calls,
            wall_ms=(time.perf_counter() - t0) * 1000.0,
        )
        self.last_cost = total_cost

        # Cap total selected tools to cover all sub-goals
        limit = max(k, len(sub_goals) * 2, self.max_total) if k > 0 else self.max_total
        final_specs = [self.catalog[i] for i in selected_indices[:limit]]
        return final_specs
