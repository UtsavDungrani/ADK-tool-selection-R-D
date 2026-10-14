"""Agent for the `adk web` dropdown: random selection strategy."""

try:
    from _common import make_agent
except ImportError:
    from agents._common import make_agent

root_agent = make_agent(
    "random",
    "Random k tools - the signal floor, for sanity-checking the UI",
)
