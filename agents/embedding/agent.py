"""Agent for the `adk web` dropdown: embedding selection strategy."""

from _common import make_agent

root_agent = make_agent(
    "embedding",
    "Dense retrieval over Gemini embeddings, asymmetric query/document",
)
