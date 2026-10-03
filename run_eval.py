#!/usr/bin/env python
"""Entry point for the tool-selection sweep.

Two modes:

  --retrieval-only   Measures recall@k only. No ADK agent, no model calls, no
                     API key (except for the embedding strategy, which needs
                     one to embed). Fast, free, and enough to compare
                     retrievers against each other.

  (default)          Full sweep through a real ADK agent. Measures what the
                     model actually called, real prompt tokens and latency.
                     Needs GOOGLE_API_KEY.

Start with --retrieval-only while iterating on the catalog: if a retriever
cannot surface the gold tool, no amount of model quality will save it, and you
find that out for free.

Examples:
    python run_eval.py --retrieval-only --strategies bm25,random --sizes 100,200,400
    python run_eval.py --strategies bm25,all_tools --sizes 100 --k 5
    python run_eval.py --retrieval-only --profile base --sizes 50,400
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from catalog import load_catalog
from tasks import tasks_for

RESULTS_DIR = Path(__file__).parent / "results"


def _load_dotenv() -> None:
    """Minimal .env loader -- avoids a dependency for three lines of parsing."""
    env = Path(__file__).parent / ".env"
    if not env.exists():
        return
    for line in env.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def build_strategy(name: str, catalog, model: str, tasks):
    from strategies.embedding import EmbeddingStrategy
    from strategies.hierarchical import HierarchicalStrategy
    from strategies.lexical import (
        AllToolsStrategy,
        BM25Strategy,
        OracleStrategy,
        RandomStrategy,
    )

    if name == "all_tools":
        return AllToolsStrategy(catalog)
    if name == "random":
        return RandomStrategy(catalog)
    if name == "bm25":
        return BM25Strategy(catalog)
    if name == "embedding":
        return EmbeddingStrategy(catalog)
    if name == "embedding_symmetric":
        return EmbeddingStrategy(catalog, asymmetric=False)
    if name == "hierarchical":
        return HierarchicalStrategy(catalog, model=model)
    if name == "oracle":
        return OracleStrategy(catalog, {t.query.strip(): t.gold for t in tasks})
    raise SystemExit(f"unknown strategy: {name}")


# ---------------------------------------------------------------- retrieval
def run_retrieval_only(args) -> list[dict]:
    from tasks import TIERS

    tasks = tasks_for(args.profile)
    rows: list[dict] = []
    ks = [int(k) for k in args.k_sweep.split(",")]
    for size in args.sizes:
        catalog = load_catalog(size, seed=args.seed, profile=args.profile)
        for sname in args.strategies:
            strat = build_strategy(sname, catalog, args.model, tasks)
            strat.warmup()
            for k in ks:
                hits = {t.id: t.gold in {s.name for s in strat.select(t.query, k)} for t in tasks}
                row = {
                    "mode": "retrieval",
                    "profile": args.profile,
                    "strategy": sname,
                    "catalog_size": size,
                    "k": k,
                    "recall": round(sum(hits.values()) / len(tasks), 4),
                }
                for tier in TIERS:
                    sub = [t for t in tasks if t.tier == tier]
                    row[f"recall_{tier}"] = round(
                        sum(hits[t.id] for t in sub) / len(sub), 4
                    )
                rows.append(row)
                print(
                    f"  size={size:<4} {sname:<20} k={k:<3} "
                    f"recall={row['recall']:.3f}  "
                    f"(easy {row['recall_easy']:.2f} / "
                    f"med {row['recall_medium']:.2f} / "
                    f"hard {row['recall_hard']:.2f})"
                )
    return rows


# --------------------------------------------------------------------- full
async def run_full(args) -> tuple[list[dict], list[dict]]:
    from google.adk.sessions import InMemorySessionService

    from harness.metrics import by_tier, confusion, summarize
    from harness.runner import run_task
    from strategies.base import StrategyToolset

    if not (os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")):
        raise SystemExit(
            "No GOOGLE_API_KEY found. Copy .env.example to .env and add your key, "
            "or use --retrieval-only."
        )

    tasks = tasks_for(args.profile)
    summaries: list[dict] = []
    per_task: list[dict] = []

    for size in args.sizes:
        catalog = load_catalog(size, seed=args.seed, profile=args.profile)
        for sname in args.strategies:
            strat = build_strategy(sname, catalog, args.model, tasks)
            strat.warmup()
            k = len(catalog) if sname == "all_tools" else args.k
            toolset = StrategyToolset(strat, k=k)
            session_service = InMemorySessionService()

            results = []
            for i, task in enumerate(tasks, 1):
                r = await run_task(task, toolset, args.model, session_service)
                results.append(r)
                per_task.append({"strategy": sname, "catalog_size": size, **r.as_row()})
                mark = "OK " if r.correct else ("ERR" if r.error else "   ")
                print(
                    f"  [{i:>2}/{len(tasks)}] {mark} {task.id:<6} {sname:<14} "
                    f"size={size:<4} declared={r.declared_count:<4} "
                    f"gold={task.gold:<32} chose={r.chosen}"
                )
                if args.sleep:
                    await asyncio.sleep(args.sleep)

            s = summarize(results, sname, size, k)
            row = s.as_row()
            row["tiers"] = json.dumps(by_tier(results))
            summaries.append(row)
            print(
                f"\n  == {sname} size={size}: acc={s.accuracy:.3f} "
                f"recall={s.recall:.3f} acc|recall={s.accuracy_given_recall:.3f} "
                f"trap={s.trap_rate:.3f} tokens={s.mean_total_prompt_tokens:.0f} "
                f"p50={s.p50_latency_ms:.0f}ms\n"
            )
            top_conf = confusion(results, top=5)
            if top_conf:
                print("  top confusions (gold -> chosen):")
                for g, ch, n in top_conf:
                    print(f"    {n}x  {g} -> {ch}")
                print()

    return summaries, per_task


def write_csv(rows: list[dict], path: Path) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for r in rows:
        for key in r:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {path}  ({len(rows)} rows)")


def main() -> int:
    _load_dotenv()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--strategies", default="bm25,random",
                   help="comma-separated: all_tools,random,bm25,embedding,embedding_symmetric,hierarchical,oracle")
    p.add_argument("--sizes", default="100", help="comma-separated catalog sizes, e.g. 100,200,400")
    p.add_argument("--profile", default="full", choices=["base", "full"],
                   help="which hand-written core: base=50 tools/60 tasks, full=100/120")
    p.add_argument("--k", type=int, default=5, help="tools declared per request (full mode)")
    p.add_argument("--k-sweep", dest="k_sweep", default="1,3,5,10,20",
                   help="k values to measure in --retrieval-only mode")
    p.add_argument("--model", default="gemini-3.5-flash-lite")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--retrieval-only", action="store_true")
    p.add_argument("--sleep", type=float, default=0.0,
                   help="seconds between tasks, to stay under rate limits")
    p.add_argument("--tag", default="", help="suffix for the output filenames")
    args = p.parse_args()

    args.strategies = [s.strip() for s in args.strategies.split(",") if s.strip()]
    args.sizes = [int(s) for s in args.sizes.split(",")]

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    tag = f"_{args.tag}" if args.tag else ""

    if args.retrieval_only:
        print(f"retrieval-only sweep: strategies={args.strategies} sizes={args.sizes}\n")
        rows = run_retrieval_only(args)
        write_csv(rows, RESULTS_DIR / f"retrieval_{stamp}{tag}.csv")
    else:
        print(f"full sweep: strategies={args.strategies} sizes={args.sizes} k={args.k}\n")
        summaries, per_task = asyncio.run(run_full(args))
        write_csv(summaries, RESULTS_DIR / f"summary_{stamp}{tag}.csv")
        write_csv(per_task, RESULTS_DIR / f"pertask_{stamp}{tag}.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
