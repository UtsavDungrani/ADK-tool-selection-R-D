#!/usr/bin/env python
"""Run ONE query against every strategy and print a side-by-side comparison.

This is the demo tool. `run_eval.py` produces the real numbers over 60 tasks;
this answers "what does each strategy do with *this* query" in a few seconds,
which is what you want when showing someone the idea or debugging a single
confusing case.

It talks to a running `adk web` / `adk api_server` over HTTP, so it exercises
exactly the same agents the dev UI serves -- no separate code path that could
drift from what you demo.

ACCOUNTING CAVEAT -- this tool is for demos, not for the write-up.

Two deliberate simplifications make its numbers differ from `run_eval.py`:

  1. It reports the prompt tokens of the FIRST model call only. `run_eval.py`
     sums every call in the turn, including the follow-up after the stub tool
     returns. First-call-only isolates the cost of *declaring* tools; the sum
     is the true cost of the turn. Expect roughly a 2x gap on the same query.
  2. It cannot see a strategy's own spend. `hierarchical` makes a router call
     before any tool is declared, and that is invisible over this HTTP API, so
     hierarchical looks cheaper here than it is. `run_eval.py` tracks it via
     `aux_cost` and adds it back.

Quote `run_eval.py` numbers in the report. Use these to build intuition.

Usage:
    adk web agents --port 8001          # in another terminal
    python compare_query.py "Our repo acme/infra needs sam to be able to merge."
    python compare_query.py --gold github_add_collaborator "..."
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request

DEFAULT_BASE = "http://127.0.0.1:8001"
DEFAULT_APPS = ["all_tools", "bm25", "embedding", "hierarchical", "rag_multi_tool", "random_floor"]



def _post(url: str, payload: dict, timeout: float = 120.0):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read().decode("utf-8")
    return json.loads(body) if body.strip() else None


def run_one(base: str, app: str, query: str, timeout: float) -> dict:
    sid = f"cmp-{app}-{int(time.time() * 1000)}"
    out: dict = {"app": app}
    t0 = time.perf_counter()
    try:
        _post(f"{base}/apps/{app}/users/u1/sessions/{sid}", {}, timeout)
        events = _post(
            f"{base}/run",
            {
                "appName": app,
                "userId": "u1",
                "sessionId": sid,
                "newMessage": {"role": "user", "parts": [{"text": query}]},
            },
            timeout,
        ) or []
    except urllib.error.HTTPError as e:
        out["error"] = f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:160]}"
        return out
    except Exception as exc:  # noqa: BLE001
        out["error"] = f"{type(exc).__name__}: {exc}"
        return out
    out["latency_ms"] = (time.perf_counter() - t0) * 1000.0

    for ev in events:
        for p in (ev.get("content") or {}).get("parts") or []:
            if p.get("functionCall") and "called" not in out:
                out["called"] = p["functionCall"]["name"]
                out["args"] = p["functionCall"].get("args", {})
            if p.get("text"):
                out.setdefault("text", p["text"].strip())
        sd = (ev.get("actions") or {}).get("stateDelta") or {}
        if sd.get("declared_count") is not None and "declared_count" not in out:
            out["declared_count"] = sd["declared_count"]
            out["declared_tools"] = sd.get("declared_tools")
        um = ev.get("usageMetadata")
        if um and "prompt_tokens" not in out:
            out["prompt_tokens"] = um.get("promptTokenCount")
    return out


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("query")
    p.add_argument("--base", default=DEFAULT_BASE)
    p.add_argument("--apps", default=",".join(DEFAULT_APPS))
    p.add_argument("--gold", default=None, help="expected tool, to mark correctness")
    p.add_argument("--timeout", type=float, default=120.0)
    p.add_argument("--show-declared", action="store_true", help="print each declared tool set")
    args = p.parse_args()

    apps = [a.strip() for a in args.apps.split(",") if a.strip()]
    print(f"query: {args.query}")
    if args.gold:
        print(f"gold : {args.gold}")
    print(f"base : {args.base}\n")

    hdr = f"{'strategy':<14} {'declared':>8} {'tokens':>7} {'ms':>7}  {'called':<34} {'':<7}"
    print(hdr)
    print("-" * len(hdr))

    rows = []
    for app in apps:
        r = run_one(args.base, app, args.query, args.timeout)
        rows.append(r)
        if "error" in r:
            print(f"{app:<14} {'-':>8} {'-':>7} {'-':>7}  ERROR: {r['error']}")
            continue
        called = r.get("called") or "(no tool call)"
        verdict = ""
        if args.gold:
            verdict = "CORRECT" if called == args.gold else "wrong"
        print(
            f"{app:<14} {r.get('declared_count', '?'):>8} "
            f"{r.get('prompt_tokens', '?'):>7} {r.get('latency_ms', 0):>7.0f}  "
            f"{called:<34} {verdict:<7}"
        )

    if args.show_declared:
        print()
        for r in rows:
            if r.get("declared_tools"):
                print(f"{r['app']}:")
                for t in r["declared_tools"]:
                    mark = " <-- gold" if args.gold and t == args.gold else ""
                    print(f"    {t}{mark}")

    # The headline comparison: tokens spent per strategy against the baseline.
    base_row = next((r for r in rows if r["app"] == "all_tools" and "prompt_tokens" in r), None)
    if base_row:
        print(f"\nbaseline (all_tools) prompt tokens: {base_row['prompt_tokens']}")
        for r in rows:
            if r["app"] == "all_tools" or "prompt_tokens" not in r:
                continue
            saved = base_row["prompt_tokens"] - r["prompt_tokens"]
            pct = 100.0 * saved / base_row["prompt_tokens"] if base_row["prompt_tokens"] else 0
            print(f"  {r['app']:<14} {r['prompt_tokens']:>6}  ({saved:+d}, {pct:+.0f}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
