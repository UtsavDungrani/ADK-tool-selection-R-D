"""Strategies that need no API key: the controls and the lexical baseline.

These four bracket every result you will get:

  AllTools   Declare the whole catalog. The unoptimised status quo, and the
             accuracy ceiling you are allowed to lose against -- any strategy
             that beats AllTools on accuracy is suspicious until explained.
  Random     Declare k tools at random. The floor. If a real strategy is not
             far above this, it has no signal.
  BM25       Classic sparse keyword retrieval. The baseline people skip, and
             then publish embedding numbers with nothing to compare against.
  Oracle     Declare exactly the gold tool. The ceiling for any retriever.
             Gap between Oracle and your strategy = retrieval headroom.

Report all four. A single embedding number with no brackets says nothing.
"""

from __future__ import annotations

import math
import random
import re
from collections import Counter

from catalog import ToolSpec

from .base import AuxCost, SelectionStrategy

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    """Lowercase alphanumeric tokens.

    Splitting on non-alphanumerics means snake_case tool names fall apart for
    free: "github_create_issue" -> ["github", "create", "issue"]. That is a
    large part of why BM25 is competitive on this catalog, and it is worth
    naming in the write-up rather than letting the number look like magic.
    """
    return _TOKEN_RE.findall(text.lower())


class AllToolsStrategy(SelectionStrategy):
    name = "all_tools"
    description = "Declare the entire catalog on every request (no selection)."

    def select(self, query: str, k: int) -> list[ToolSpec]:
        self.last_cost = AuxCost()
        return list(self.catalog)


class RandomStrategy(SelectionStrategy):
    name = "random"
    description = "Declare k tools chosen uniformly at random (signal floor)."

    def __init__(self, catalog: list[ToolSpec], seed: int = 0):
        super().__init__(catalog)
        self.seed = seed

    def select(self, query: str, k: int) -> list[ToolSpec]:
        self.last_cost = AuxCost()
        # Seeded on the query so a given query is stable across runs, while
        # different queries still get different draws.
        rng = random.Random(f"{self.seed}:{query}")
        return rng.sample(self.catalog, min(k, len(self.catalog)))


class OracleStrategy(SelectionStrategy):
    name = "oracle"
    description = "Declare only the gold tool (retrieval ceiling, not deployable)."

    def __init__(self, catalog: list[ToolSpec], gold_by_query: dict[str, str]):
        super().__init__(catalog)
        self.gold_by_query = gold_by_query

    def select(self, query: str, k: int) -> list[ToolSpec]:
        self.last_cost = AuxCost()
        gold = self.gold_by_query.get(query.strip())
        if gold is None or gold not in self.by_name:
            raise KeyError(
                f"OracleStrategy has no gold label for query {query!r}. "
                "The oracle must never guess -- fix the query mapping."
            )
        return [self.by_name[gold]]


class BM25Strategy(SelectionStrategy):
    """Okapi BM25 over tool name + description + parameter text."""

    name = "bm25"
    description = "Sparse keyword retrieval (Okapi BM25) over tool text."

    def __init__(self, catalog: list[ToolSpec], k1: float = 1.5, b: float = 0.75):
        super().__init__(catalog)
        self.k1 = k1
        self.b = b
        self._docs: list[list[str]] = []
        self._tf: list[Counter] = []
        self._idf: dict[str, float] = {}
        self._avg_len = 0.0

    def warmup(self) -> None:
        self._docs = [tokenize(s.index_text()) for s in self.catalog]
        self._tf = [Counter(d) for d in self._docs]
        n = len(self._docs)
        self._avg_len = sum(len(d) for d in self._docs) / max(n, 1)

        df: Counter = Counter()
        for d in self._docs:
            df.update(set(d))
        # Robertson/Sparck-Jones IDF with the +1 smoothing that keeps it
        # non-negative for terms appearing in most documents.
        self._idf = {
            term: math.log(1 + (n - freq + 0.5) / (freq + 0.5))
            for term, freq in df.items()
        }

    def _score(self, q_tokens: list[str], idx: int) -> float:
        tf = self._tf[idx]
        dl = len(self._docs[idx])
        score = 0.0
        for t in q_tokens:
            f = tf.get(t)
            if not f:
                continue
            idf = self._idf.get(t, 0.0)
            denom = f + self.k1 * (1 - self.b + self.b * dl / max(self._avg_len, 1e-9))
            score += idf * (f * (self.k1 + 1)) / denom
        return score

    def select(self, query: str, k: int) -> list[ToolSpec]:
        self.last_cost = AuxCost()
        if not self._docs:
            self.warmup()
        q = tokenize(query)
        scored = [(self._score(q, i), i) for i in range(len(self.catalog))]
        # Tie-break on catalog index so results are deterministic; without this
        # Python's stable sort still depends on construction order and a
        # reordered catalog would silently change the numbers.
        scored.sort(key=lambda si: (-si[0], si[1]))
        return [self.catalog[i] for _, i in scored[:k]]
