"""Agent for the `adk web` dropdown: all_tools selection strategy."""

try:
    from _common import make_agent
except ImportError:
    from agents._common import make_agent

root_agent = make_agent(
    "all_tools",
    "Declares the entire catalog every turn - the unoptimised baseline",
)
