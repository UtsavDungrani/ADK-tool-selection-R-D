"""Dense retrieval over tool descriptions using Gemini embeddings.

Two details here are easy to get wrong and both materially change the numbers:

1. ASYMMETRIC EMBEDDING. Tool descriptions are embedded with
   task_type=RETRIEVAL_DOCUMENT and user queries with RETRIEVAL_QUERY. Gemini's
   embedding models are trained for this split; embedding both sides the same
   way ("symmetric") is the single most common mistake in tool-retrieval code
   and it costs real recall. If you want to measure that, flip `asymmetric` to
   False and rerun -- it is a legitimate ablation, not a bug.

2. CACHING. The catalog is embedded once and cached on disk, keyed by
   (model, task_type, text). Re-running the sweep therefore costs nothing for
   documents, and query embeddings are cached too since the 60 tasks repeat
   across every configuration. Without this the sweep would issue thousands of
   redundant embedding calls, and the latency column would measure the network
   rather than the strategy.

Cost accounting: embedding calls are real spend, so each `select` reports
`embed_calls` in `last_cost`. A cache hit costs zero and is reported as zero --
which is correct for a warm production system and optimistic for a cold one.
Note that distinction in the write-up.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import time
from pathlib import Path

from catalog import ToolSpec

from .base import AuxCost, SelectionStrategy

_CACHE_PATH = Path(__file__).resolve().parent.parent / "results" / ".embed_cache.json"
_DEFAULT_MODEL = "gemini-embedding-001"


class EmbeddingCache:
    """Disk-backed embedding cache. Plain JSON -- small, and easy to inspect."""

    def __init__(self, path: Path = _CACHE_PATH):
        self.path = path
        self._data: dict[str, list[float]] = {}
        if path.exists():
            try:
                self._data = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                # A corrupt cache must never fail a run; rebuild it.
                self._data = {}
        self._dirty = False

    @staticmethod
    def key(model: str, task_type: str, text: str) -> str:
        h = hashlib.sha256(f"{model}|{task_type}|{text}".encode("utf-8")).hexdigest()
        return h[:32]

    def get(self, model: str, task_type: str, text: str) -> list[float] | None:
        return self._data.get(self.key(model, task_type, text))

    def put(self, model: str, task_type: str, text: str, vec: list[float]) -> None:
        self._data[self.key(model, task_type, text)] = vec
        self._dirty = True

    def flush(self) -> None:
        if not self._dirty:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self._data), encoding="utf-8")
        self._dirty = False


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


class EmbeddingStrategy(SelectionStrategy):
    name = "embedding"
    description = "Dense retrieval: cosine similarity over Gemini tool embeddings."

    def __init__(
        self,
        catalog: list[ToolSpec],
        model: str = _DEFAULT_MODEL,
        asymmetric: bool = True,
        cache: EmbeddingCache | None = None,
        batch_size: int = 64,
    ):
        super().__init__(catalog)
        self.model = model
        self.asymmetric = asymmetric
        self.cache = cache or EmbeddingCache()
        self.batch_size = batch_size
        self._doc_vecs: list[list[float]] = []
        self._client = None
        self.name = "embedding" if asymmetric else "embedding_symmetric"

    # -- client -----------------------------------------------------------
    def _get_client(self):
        if self._client is None:
            from google import genai

            api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
            if not api_key:
                raise RuntimeError(
                    "EmbeddingStrategy needs GOOGLE_API_KEY (or GEMINI_API_KEY). "
                    "Copy .env.example to .env and fill it in, or run with "
                    "--strategies bm25,random to stay offline."
                )
            self._client = genai.Client(api_key=api_key)
        return self._client

    def _embed(self, texts: list[str], task_type: str) -> tuple[list[list[float]], int]:
        """Embed `texts`, using the cache. Returns (vectors, api_call_count)."""
        from google.genai import types

        out: list[list[float] | None] = [
            self.cache.get(self.model, task_type, t) for t in texts
        ]
        missing = [i for i, v in enumerate(out) if v is None]
        api_calls = 0

        for start in range(0, len(missing), self.batch_size):
            chunk_idx = missing[start : start + self.batch_size]
            chunk = [texts[i] for i in chunk_idx]
            resp = self._get_client().models.embed_content(
                model=self.model,
                contents=chunk,
                config=types.EmbedContentConfig(task_type=task_type),
            )
            api_calls += 1
            for i, emb in zip(chunk_idx, resp.embeddings):
                vec = list(emb.values)
                out[i] = vec
                self.cache.put(self.model, task_type, texts[i], vec)
            # Flush per batch, not once at the end. Warming a 350-tool catalog
            # is hundreds of embed requests and the free tier caps them per
            # minute, so a 429 part-way through is normal. Flushing here means
            # the next attempt resumes instead of starting over.
            self.cache.flush()

        if api_calls:
            self.cache.flush()
        return [v for v in out if v is not None], api_calls

    # -- strategy ---------------------------------------------------------
    def warmup(self) -> None:
        doc_task = "RETRIEVAL_DOCUMENT" if self.asymmetric else "SEMANTIC_SIMILARITY"
        texts = [s.index_text() for s in self.catalog]
        self._doc_vecs, _ = self._embed(texts, doc_task)

    def select(self, query: str, k: int) -> list[ToolSpec]:
        t0 = time.perf_counter()
        if not self._doc_vecs:
            self.warmup()
        q_task = "RETRIEVAL_QUERY" if self.asymmetric else "SEMANTIC_SIMILARITY"
        qv, calls = self._embed([query], q_task)
        scored = [(_cosine(qv[0], dv), i) for i, dv in enumerate(self._doc_vecs)]
        scored.sort(key=lambda si: (-si[0], si[1]))
        self.last_cost = AuxCost(
            embed_calls=calls,
            wall_ms=(time.perf_counter() - t0) * 1000.0,
        )
        return [self.catalog[i] for _, i in scored[:k]]
