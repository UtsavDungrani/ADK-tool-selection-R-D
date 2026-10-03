"""Agent for the `adk web` dropdown: all_tools selection strategy."""

from _common import make_agent

root_agent = make_agent(
    "all_tools",
    "Declares the entire catalog every turn - the unoptimised baseline",
)
