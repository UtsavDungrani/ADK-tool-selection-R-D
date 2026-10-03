"""Shared agent factory for the `adk web` dev UI.

WHY ONE FOLDER PER STRATEGY

`adk web` lists every subdirectory of the agents dir in a dropdown. By giving
each selection strategy its own folder, that dropdown becomes a live strategy
switcher: type the same query, flip the dropdown, and watch the declared tool
surface and the model's choice change. It is the fastest way to build intuition
before committing to a full sweep -- and it demos well.

WHAT TO LOOK AT IN THE UI

  Events tab   The functionCall shows which tool the model chose. That is the
               selection signal the whole project measures.
  State tab    `declared_tools` / `declared_count` are written there by the
               before_model_callback below, so you can see what the strategy
               actually exposed for that turn -- the input to the model's
               decision, not just its output.
  Trace tab    Per-step latency, including the hierarchical router's extra
               call.

Reading State alongside Events is the point. If the gold tool is missing from
`declared_tools`, the retriever failed. If it is present and the model still
picked wrong, the retriever is fine and the descriptions are not.

CONFIG

  TSRND_PROFILE        "base" (50 core tools) or "full" (100), default full
  TSRND_CATALOG_SIZE   total catalog size incl. filler, default = core size
  TSRND_K              tools declared per request, default 5

Set these in the project `.env` and restart `adk web` to compare sizes.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# The agent packages are imported by ADK from the agents/ directory, so the
# project root is not on sys.path by default. Add it so `catalog` and
# `strategies` resolve.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from google.adk.agents import LlmAgent  # noqa: E402

from catalog import load_catalog  # noqa: E402
from strategies.base import StrategyToolset  # noqa: E402

DEFAULT_MODEL = "gemini-3.5-flash-lite"

INSTRUCTION = """You are a tool router.

Given the user's request, call exactly ONE tool that best fulfils it.

Rules:
- Always call a tool. Never answer in prose.
- Never ask a clarifying question.
- If an argument's value is not stated in the request, supply a reasonable
  placeholder. Argument values are not evaluated; choosing the right tool is.

After the tool returns, reply with one short line naming the tool you chose
and why it was the right one over the closest alternative.
"""


def _profile() -> str:
    return os.environ.get("TSRND_PROFILE", "full")


def _catalog_size() -> int:
    """Total catalog size. Defaults to the profile's core (no filler padding)."""
    raw = os.environ.get("TSRND_CATALOG_SIZE")
    if raw:
        return int(raw)
    from catalog import PROFILES

    return len(PROFILES[_profile()])


def _k() -> int:
    return int(os.environ.get("TSRND_K", "5"))


def _build_strategy(name: str, catalog, model: str):
    from strategies.embedding import EmbeddingStrategy
    from strategies.hierarchical import HierarchicalStrategy
    from strategies.lexical import AllToolsStrategy, BM25Strategy, RandomStrategy

    if name == "all_tools":
        return AllToolsStrategy(catalog)
    if name == "random":
        return RandomStrategy(catalog)
    if name == "bm25":
        return BM25Strategy(catalog)
    if name == "embedding":
        return EmbeddingStrategy(catalog)
    if name == "hierarchical":
        return HierarchicalStrategy(catalog, model=model)
    raise ValueError(f"unknown strategy: {name}")


def _make_capture(strategy_name: str):
    """Surface the declared tool set in the UI's State tab."""

    def capture(callback_context, llm_request):  # noqa: ANN001 - ADK signature
        decls = []
        for tool in (getattr(llm_request.config, "tools", None) or []):
            decls.extend(getattr(tool, "function_declarations", None) or [])
        names = [d.name for d in decls]
        try:
            callback_context.state["strategy"] = strategy_name
            callback_context.state["declared_count"] = len(names)
            # Full list for small surfaces; a head for large ones, so the State
            # tab stays readable when all_tools declares the whole catalog.
            callback_context.state["declared_tools"] = (
                names if len(names) <= 25 else names[:25] + [f"... +{len(names) - 25} more"]
            )
        except Exception:  # noqa: BLE001 - never break a turn over telemetry
            pass
        return None

    return capture


def make_agent(strategy_name: str, description: str) -> LlmAgent:
    model = os.environ.get("TSRND_MODEL", DEFAULT_MODEL)
    catalog = load_catalog(_catalog_size(), profile=_profile())
    strategy = _build_strategy(strategy_name, catalog, model)
    strategy.warmup()

    k = len(catalog) if strategy_name == "all_tools" else _k()
    toolset = StrategyToolset(strategy, k=k)

    return LlmAgent(
        model=model,
        name=f"{strategy_name}_selector",
        description=f"{description} (catalog={len(catalog)}, k={k})",
        instruction=INSTRUCTION,
        tools=[toolset],
        before_model_callback=_make_capture(strategy_name),
    )
