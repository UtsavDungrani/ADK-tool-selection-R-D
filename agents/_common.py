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
  Graph tab    The nodes are the catalog -- everything the agent can reach,
               not what this turn used. ADK fetches the structure once per
               app selection, so it cannot track the prompt; the per-turn
               answer is the green highlighting, which the UI computes from
               the selected invocation's function calls. See
               `CatalogProjectedTools` for why it has to be this way.

Reading State alongside Events is the point. If the gold tool is missing from
`declared_tools`, the retriever failed. If it is present and the model still
picked wrong, the retriever is fine and the descriptions are not.

CONFIG

  TSRND_PROFILE        "base" (50 core tools) or "full" (100), default full
  TSRND_CATALOG_SIZE   total catalog size incl. filler, default = core size
  TSRND_K              tools declared per request, default 5
  TSRND_GRAPH          "catalog" (default) draws every reachable tool in the
                       Graph tab; "toolset" draws the single dynamic-toolset
                       node instead. Use "toolset" -- or a smaller profile --
                       when a 350-node graph is more than the pane can show.

Set these in the project `.env` and restart `adk web` to compare sizes.
"""

from __future__ import annotations

import json
import os
import sqlite3
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

MULTI_TOOL_INSTRUCTION = """You are an agent equipped with specialized enterprise tools.

Given the user's request:
1. Identify all operations and services requested (GitHub, Slack, Jira, Google Calendar, Google Drive, Stripe, etc.).
2. You MUST invoke a tool for EVERY single requested operation. NEVER describe, simulate, or defer an action in text without executing its corresponding tool.
3. CRITICAL: Execute tools sequentially, calling exactly ONE tool per step in logical pipeline order. Do NOT call multiple tools in parallel in the same turn. Wait for the tool's result before proceeding to invoke the next tool.
4. If an argument's value is not stated in the request, supply a reasonable placeholder.
5. Only after all tools have finished executing sequentially one by one, reply with a concise summary of the operations performed.
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
    if name == "rag_multi":
        from strategies.rag_multi import RAGMultiToolStrategy

        return RAGMultiToolStrategy(catalog, decomposer_model=model)
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


#: Modules of ADK's dev UI that read `agent.tools` to draw a picture rather
#: than to run a turn. Nothing else may see the projection below.
_GRAPH_MODULES = ("graph_serialization", "agent_graph")


def _called_from_graph_code() -> bool:
    """True when the current call stack is ADK drawing the agent graph.

    `agent.tools` has two readers with incompatible needs: the runtime, which
    must get the single dynamic toolset, and the dev UI's graph serializer,
    which can only draw what it is handed and would otherwise render one
    opaque `StrategyToolset` box. ADK offers no separate hook for the second,
    so the reader is identified by its frame.

    Walks frames directly rather than using `inspect.stack()`, which resolves
    source context for every frame on the stack and is far too expensive for
    something on the tool-resolution path.
    """
    frame = sys._getframe(1)
    depth = 0
    while frame is not None and depth < 40:
        name = frame.f_code.co_filename
        for module in _GRAPH_MODULES:
            if module in name:
                return True
        frame = frame.f_back
        depth += 1
    return False


def _tool_callback(tool, args, tool_context):  # noqa: ANN001
    """Record executed tool name into state and invocation tracker."""
    name = getattr(tool, "name", None) or getattr(tool, "__name__", str(tool))
    invoc_id = getattr(tool_context, "invocation_id", None) if tool_context else None
    if name:
        from tools._adk import record_tool_used

        record_tool_used(name, invocation_id=invoc_id)
    if tool_context and hasattr(tool_context, "state"):
        try:
            used = tool_context.state.get("used_tools", [])
            if name and name not in used:
                tool_context.state["used_tools"] = [*used, name]
        except Exception:
            pass
    return None


class CatalogProjectedTools(list):
    """Runtime tool list that renders only used tools in ADK's structure graph.

    At runtime during execution turns, this yields `self.toolset` so ADK
    executes with dynamic selection.

    When ADK's graph serialization / visualization code inspects `agent.tools`,
    this yields only the tools that were actually used (invoked) by the agent.
    If no tools have been used yet, it returns an empty list so the graph
    displays cleanly without hundreds of distracting, unused catalog nodes.

    Override via `TSRND_GRAPH`:
      "used" (default) -> only show used tools
      "catalog"        -> show all tools in the catalog
      "toolset"        -> show single StrategyToolset node
    """

    def __init__(
        self,
        toolset: StrategyToolset,
        catalog,
        agent_dir: Optional[Path] = None,
    ):
        super().__init__([toolset])
        self.toolset = toolset
        self.catalog = list(catalog)
        self.specs_by_name = {s.name: s for s in self.catalog}
        self.agent_dir = agent_dir

    def _get_projected_tools(self) -> list:
        mode = os.environ.get("TSRND_GRAPH", "used").strip().lower()
        if mode == "toolset":
            return []
        if mode == "catalog":
            from catalog import build_tools

            return list(build_tools(self.catalog))

        # Default mode: "used" -> only show used tools for the latest prompt (invocation)
        from catalog import build_tools
        from tools import ALL_SPECS
        from tools._adk import get_recorded_tool_names

        used_names: list[str] = []
        latest_invoc_id: Optional[str] = None

        # 1. Inspect the agent's .adk/session.db for the latest invocation
        if self.agent_dir:
            db_path = self.agent_dir / ".adk" / "session.db"
            if db_path.exists():
                try:
                    conn = sqlite3.connect(str(db_path))
                    row = conn.execute(
                        "SELECT invocation_id FROM events ORDER BY timestamp DESC LIMIT 1"
                    ).fetchone()
                    if row and row[0]:
                        latest_invoc_id = row[0]
                        events = conn.execute(
                            "SELECT event_data FROM events WHERE invocation_id=? ORDER BY timestamp ASC",
                            (latest_invoc_id,),
                        ).fetchall()
                        for (event_json,) in events:
                            try:
                                data = json.loads(event_json)
                                parts = data.get("content", {}).get("parts", [])
                                for p in parts:
                                    if "function_call" in p:
                                        t_name = p["function_call"].get("name")
                                        if t_name and t_name not in used_names:
                                            used_names.append(t_name)
                            except Exception:
                                pass
                    conn.close()
                except Exception:
                    pass

        # 2. Also merge in-memory tools recorded for this invocation
        in_memory_tools = get_recorded_tool_names(invocation_id=latest_invoc_id)
        for t_name in in_memory_tools:
            if t_name not in used_names:
                used_names.append(t_name)

        all_specs_by_name = {s.name: s for s in ALL_SPECS}
        used_specs = []
        for name in used_names:
            spec = self.specs_by_name.get(name) or all_specs_by_name.get(name)
            if spec:
                used_specs.append(spec)

        return list(build_tools(used_specs))

    def __iter__(self):
        if _called_from_graph_code():
            return iter(self._get_projected_tools())
        return super().__iter__()


def make_agent(strategy_name: str, description: str) -> LlmAgent:
    model = os.environ.get("TSRND_MODEL", DEFAULT_MODEL)
    catalog = load_catalog(_catalog_size(), profile=_profile())
    strategy = _build_strategy(strategy_name, catalog, model)
    strategy.warmup()

    k = len(catalog) if strategy_name == "all_tools" else _k()
    toolset = StrategyToolset(strategy, k=k)

    agent_dir = Path(__file__).resolve().parent / strategy_name
    tools_wrapper = CatalogProjectedTools(toolset, catalog, agent_dir=agent_dir)

    agent = LlmAgent(
        model=model,
        name=f"{strategy_name}_selector",
        description=f"{description} (catalog={len(catalog)}, k={k})",
        instruction=INSTRUCTION,
        tools=[toolset],
        before_model_callback=_make_capture(strategy_name),
        before_tool_callback=_tool_callback,
    )
    # Direct assignment: Pydantic validation would degrade the subclass into a
    # plain list and the graph would lose the projection.
    agent.tools = tools_wrapper
    return agent


def make_static_agent(description: str) -> LlmAgent:
    """Build the all-tools agent with a FLAT tool list rather than a toolset."""
    from catalog import build_tools, load_catalog

    model = os.environ.get("TSRND_MODEL", DEFAULT_MODEL)
    catalog = load_catalog(_catalog_size(), profile=_profile())
    return LlmAgent(
        model=model,
        name="all_tools_static_selector",
        description=f"{description} (catalog={len(catalog)})",
        instruction=INSTRUCTION,
        tools=list(build_tools(catalog)),
        before_model_callback=_make_capture("all_tools_static"),
    )


def make_multi_tool_agent(description: str) -> LlmAgent:
    """Build a multi-action agent backed by RAG query decomposition & vector retrieval."""
    model = os.environ.get("TSRND_MODEL", DEFAULT_MODEL)
    catalog = load_catalog(_catalog_size(), profile=_profile())
    strategy = _build_strategy("rag_multi", catalog, model)
    strategy.warmup()

    toolset = StrategyToolset(strategy, k=15)
    agent_dir = Path(__file__).resolve().parent / "rag_multi_tool"
    tools_wrapper = CatalogProjectedTools(toolset, catalog, agent_dir=agent_dir)

    agent = LlmAgent(
        model=model,
        name="rag_multi_tool_selector",
        description=f"{description} (catalog={len(catalog)}, dynamic RAG)",
        instruction=MULTI_TOOL_INSTRUCTION,
        tools=[toolset],
        before_model_callback=_make_capture("rag_multi"),
        before_tool_callback=_tool_callback,
    )
    # Direct assignment: Pydantic validation would degrade the subclass into a
    # plain list and the graph would lose the projection.
    agent.tools = tools_wrapper
    return agent

