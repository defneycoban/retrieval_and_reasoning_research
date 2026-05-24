from dataclasses import asdict
from typing import Optional

import numpy as np

from app.rag.chunking import TextChunk


class InMemoryVectorStore:
    def __init__(self) -> None:
        self._chunks: list[TextChunk] = []
        self._vectors: Optional[np.ndarray] = None

    def add(self, chunks: list[TextChunk], vectors: np.ndarray) -> None:
        if not chunks:
            return
        self._chunks.extend(chunks)
        self._vectors = vectors if self._vectors is None else np.vstack([self._vectors, vectors])

    def search(self, query_vector: np.ndarray, top_k: int) -> list[dict]:
        if self._vectors is None or not self._chunks:
            return []
        scores = self._vectors @ query_vector.reshape(-1)
        order = np.argsort(scores)[::-1][:top_k]
        results = []
        for index in order:
            chunk = self._chunks[int(index)]
            payload = asdict(chunk)
            payload["score"] = float(scores[int(index)])
            results.append(payload)
        return results

    def clear(self) -> None:
        self._chunks = []
        self._vectors = None
