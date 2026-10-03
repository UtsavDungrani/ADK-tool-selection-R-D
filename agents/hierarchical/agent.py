"""Agent for the `adk web` dropdown: hierarchical selection strategy."""

from _common import make_agent

root_agent = make_agent(
    "hierarchical",
    "Two-stage: LLM routes to a namespace, then declares its tools",
)
