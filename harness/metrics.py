"""Aggregation of per-task results into reportable summaries."""

from __future__ import annotations

import statistics
from dataclasses import dataclass
from typing import Iterable, Sequence

from harness.runner import TaskResult


def _mean(xs: Sequence[float]) -> float:
    return statistics.fmean(xs) if xs else 0.0


def _p50(xs: Sequence[float]) -> float:
    return statistics.median(xs) if xs else 0.0


def _p95(xs: Sequence[float]) -> float:
    if not xs:
        return 0.0
    ordered = sorted(xs)
    idx = min(len(ordered) - 1, int(round(0.95 * (len(ordered) - 1))))
    return ordered[idx]


@dataclass
class Summary:
    strategy: str
    catalog_size: int
    k: int
    n: int

    recall: float            # gold was declared
    accuracy: float          # model called gold
    trap_rate: float         # model called the designed distractor
    no_call_rate: float
    error_rate: float

    # Of the cases where the gold tool WAS declared, how often did the model
    # still pick it? Isolates model confusion from retrieval failure.
    accuracy_given_recall: float

    mean_declared: float
    mean_prompt_tokens: float
    mean_total_prompt_tokens: float
    mean_cached_tokens: float
    p50_latency_ms: float
    p95_latency_ms: float
    mean_aux_llm_calls: float

    def as_row(self) -> dict:
        return {
            "strategy": self.strategy,
            "catalog_size": self.catalog_size,
            "k": self.k,
            "n": self.n,
            "recall": round(self.recall, 4),
            "accuracy": round(self.accuracy, 4),
            "accuracy_given_recall": round(self.accuracy_given_recall, 4),
            "trap_rate": round(self.trap_rate, 4),
            "no_call_rate": round(self.no_call_rate, 4),
            "error_rate": round(self.error_rate, 4),
            "mean_declared": round(self.mean_declared, 2),
            "mean_prompt_tokens": round(self.mean_prompt_tokens, 1),
            "mean_total_prompt_tokens": round(self.mean_total_prompt_tokens, 1),
            "mean_cached_tokens": round(self.mean_cached_tokens, 1),
            "p50_latency_ms": round(self.p50_latency_ms, 1),
            "p95_latency_ms": round(self.p95_latency_ms, 1),
            "mean_aux_llm_calls": round(self.mean_aux_llm_calls, 2),
        }


def summarize(
    results: Iterable[TaskResult], strategy: str, catalog_size: int, k: int
) -> Summary:
    rs = list(results)
    n = len(rs)
    if n == 0:
        raise ValueError("no results to summarize")

    ok = [r for r in rs if r.error is None]
    recalled = [r for r in ok if r.recall]
    # Trap rate is over tasks that HAVE a trap; dividing by all tasks would
    # dilute it with tasks where falling into a trap was impossible.
    trappable = [r for r in ok if r.trap]

    return Summary(
        strategy=strategy,
        catalog_size=catalog_size,
        k=k,
        n=n,
        recall=_mean([r.recall for r in ok]),
        accuracy=_mean([r.correct for r in ok]),
        accuracy_given_recall=_mean([r.correct for r in recalled]),
        trap_rate=_mean([r.trapped for r in trappable]),
        no_call_rate=_mean([r.no_call for r in ok]),
        error_rate=(n - len(ok)) / n,
        mean_declared=_mean([r.declared_count for r in ok]),
        mean_prompt_tokens=_mean([r.prompt_tokens for r in ok]),
        mean_total_prompt_tokens=_mean([r.total_prompt_tokens for r in ok]),
        mean_cached_tokens=_mean([r.cached_tokens for r in ok]),
        p50_latency_ms=_p50([r.latency_ms for r in ok]),
        p95_latency_ms=_p95([r.latency_ms for r in ok]),
        mean_aux_llm_calls=_mean([r.aux_llm_calls for r in ok]),
    )


def by_tier(results: Iterable[TaskResult]) -> dict[str, dict[str, float]]:
    """Per-tier accuracy and recall -- always report this alongside the blend."""
    rs = [r for r in results if r.error is None]
    out: dict[str, dict[str, float]] = {}
    for tier in ("easy", "medium", "hard"):
        sub = [r for r in rs if r.tier == tier]
        if not sub:
            continue
        out[tier] = {
            "n": len(sub),
            "recall": round(_mean([r.recall for r in sub]), 4),
            "accuracy": round(_mean([r.correct for r in sub]), 4),
        }
    return out


def confusion(results: Iterable[TaskResult], top: int = 15) -> list[tuple[str, str, int]]:
    """Most frequent (gold, chosen) mistakes. Drives catalog improvements."""
    from collections import Counter

    c: Counter = Counter()
    for r in results:
        if r.error is None and r.chosen and not r.correct:
            c[(r.gold, r.chosen)] += 1
    return [(g, ch, n) for (g, ch), n in c.most_common(top)]
