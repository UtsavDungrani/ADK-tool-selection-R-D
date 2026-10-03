"""Strategy interface and the ADK bridge.

The central design decision of this project:

    Every selection strategy is a plain Python object that maps
    (query, k) -> list[ToolSpec]. It knows nothing about ADK.

    `StrategyToolset` is the single adapter that makes any such object usable
    by an ADK agent, via `BaseToolset.get_tools(readonly_context)`.

This matters for the experiment. ADK calls `get_tools` once per request and
declares exactly what it returns, so swapping the strategy swaps the entire
tool-exposure policy while holding the agent, the model, the prompt and the
task set fixed. That is a clean single-variable ablation -- which is the whole
point of the harness.

It also means strategies are unit-testable with no API key and no agent:
`BM25Strategy().select(q, k)` is just a function call. Only the strategies that
themselves invoke an LLM (the hierarchical router) need credentials.

COST ACCOUNTING
Some strategies are not free. A hierarchical router spends an LLM call to pick
a namespace before any tool is declared. Reporting only the declaration-token
saving would flatter those strategies, so every strategy reports `aux_cost`:
work it did on its own behalf, outside the main agent call. The report adds
this back in. A strategy that saves 4k declaration tokens but spends a 600-token
router call has saved 3.4k, and the table must say so.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.base_toolset import BaseToolset

from catalog import ToolSpec, build_tools


@dataclass
class AuxCost:
    """Resources a strategy consumed on its own behalf, outside the agent call."""

    llm_calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    embed_calls: int = 0
    wall_ms: float = 0.0

    def merge(self, other: "AuxCost") -> None:
        self.llm_calls += other.llm_calls
        self.prompt_tokens += other.prompt_tokens
        self.completion_tokens += other.completion_tokens
        self.embed_calls += other.embed_calls
        self.wall_ms += other.wall_ms

    def as_dict(self) -> dict:
        return {
            "aux_llm_calls": self.llm_calls,
            "aux_prompt_tokens": self.prompt_tokens,
            "aux_completion_tokens": self.completion_tokens,
            "aux_embed_calls": self.embed_calls,
            "aux_wall_ms": round(self.wall_ms, 2),
        }


class SelectionStrategy(ABC):
    """Maps a user query to the subset of tools that should be declared."""

    #: Short identifier used as the column name in results.
    name: str = "unnamed"

    #: Human-readable one-liner for the report.
    description: str = ""

    def __init__(self, catalog: list[ToolSpec]):
        self.catalog = catalog
        self.by_name: dict[str, ToolSpec] = {s.name: s for s in catalog}
        self.last_cost = AuxCost()

    @abstractmethod
    def select(self, query: str, k: int) -> list[ToolSpec]:
        """Return at most `k` tools to declare for this query.

        Implementations must reset and populate `self.last_cost` if they spend
        anything (LLM calls, embedding calls). Pure-local strategies may leave
        it at zero.
        """

    def warmup(self) -> None:
        """Optional one-off setup (index building, embedding the catalog).

        Called once before the eval loop so that index construction is not
        charged to the first query's latency.
        """

    def __repr__(self) -> str:
        return f"<{type(self).__name__} name={self.name!r} catalog={len(self.catalog)}>"


def extract_query(readonly_context: Optional[ReadonlyContext]) -> str:
    """Pull the user's text out of an ADK ReadonlyContext.

    `user_content` is a genai Content with zero or more parts; we concatenate
    the text parts. Returns "" when there is no usable text, which callers
    treat as "no basis for selection -- fall back to declaring everything".
    """
    if readonly_context is None:
        return ""
    content = getattr(readonly_context, "user_content", None)
    if content is None:
        return ""
    parts = getattr(content, "parts", None) or []
    texts = [p.text for p in parts if getattr(p, "text", None)]
    return " ".join(texts).strip()


class StrategyToolset(BaseToolset):
    """Adapter: exposes a SelectionStrategy to an ADK agent.

    ADK invokes `get_tools` once per model request and declares precisely the
    list we return, so this is the seam where the tool surface is decided.

    `last_selection` records what was returned for the most recent request. The
    harness reads it to compute retrieval recall independently of whether the
    model then picked the right tool -- separating "the retriever never
    surfaced the answer" from "the retriever surfaced it and the model still
    chose wrong". Those two failures have completely different fixes.
    """

    def __init__(self, strategy: SelectionStrategy, k: int):
        super().__init__()
        self.strategy = strategy
        self.k = k
        self.last_selection: list[str] = []
        self.last_cost = AuxCost()
        self.calls = 0

    async def get_tools(
        self, readonly_context: Optional[ReadonlyContext] = None
    ) -> list[BaseTool]:
        self.calls += 1
        query = extract_query(readonly_context)
        if not query:
            # No query to select on. Declaring everything is the honest
            # fallback: it is what an unoptimised agent would do anyway.
            specs = list(self.catalog_specs)
        else:
            specs = self.strategy.select(query, self.k)
        self.last_selection = [s.name for s in specs]
        self.last_cost = self.strategy.last_cost
        return build_tools(specs)

    @property
    def catalog_specs(self) -> list[ToolSpec]:
        return self.strategy.catalog

    async def close(self) -> None:
        return None
