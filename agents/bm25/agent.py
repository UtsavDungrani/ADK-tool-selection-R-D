"""Agent for the `adk web` dropdown: bm25 selection strategy."""

from _common import make_agent

root_agent = make_agent(
    "bm25",
    "Sparse keyword retrieval (BM25), no API calls to select",
)
