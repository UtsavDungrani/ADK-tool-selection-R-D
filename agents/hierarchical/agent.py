"""Agent for the `adk web` dropdown: hierarchical selection strategy."""

try:
    from _common import make_agent
except ImportError:
    from agents._common import make_agent

root_agent = make_agent(
    "hierarchical",
    "Two-stage: LLM routes to a namespace, then declares its tools",
)
