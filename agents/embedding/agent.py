"""Agent for the `adk web` dropdown: embedding selection strategy."""

try:
    from _common import make_agent
except ImportError:
    from agents._common import make_agent

root_agent = make_agent(
    "embedding",
    "Dense retrieval over Gemini embeddings, asymmetric query/document",
)
