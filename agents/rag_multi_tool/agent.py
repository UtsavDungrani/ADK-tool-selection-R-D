"""Agent for the `adk web` dropdown: rag_multi_tool selection strategy."""

try:
    from _common import make_multi_tool_agent
except ImportError:
    from agents._common import make_multi_tool_agent

root_agent = make_multi_tool_agent(
    "RAG Vector + Query Decomposition: selects only needed tools across multiple steps",
)
