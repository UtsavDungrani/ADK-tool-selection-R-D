"""all_tools, but with the tools passed as a flat list instead of a toolset.

ONLY for the dev UI's structure graph. ADK's `build_graph_image` endpoint --
the one the UI's graph panel renders -- serializes `agent.tools` literally and
never calls `canonical_tools()`, so a BaseToolset shows up as a single node no
matter how many tools it holds.

Passing the tools as a flat list makes every tool appear in that graph.

This is behaviourally identical to the `all_tools` agent, and ONLY for that
agent: all_tools declares the entire catalog on every turn anyway, so there is
nothing dynamic to lose. The selecting strategies (bm25, embedding,
hierarchical) cannot be expressed this way -- their whole purpose is to return
a different tool list per query, which a static list cannot do.
"""

from _common import make_static_agent

root_agent = make_static_agent(
    "Entire catalog as a flat tool list - identical to all_tools, but every "
    "tool appears in the dev UI structure graph",
)
