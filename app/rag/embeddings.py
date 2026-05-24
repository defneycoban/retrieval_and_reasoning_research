import hashlib
import re
from abc import ABC, abstractmethod

import numpy as np


TOKEN_RE = re.compile(r"\w+", flags=re.UNICODE)


class EmbeddingModel(ABC):
    @abstractmethod
    def encode(self, texts: list[str]) -> np.ndarray:
        raise NotImplementedError


class HashingEmbeddingModel(EmbeddingModel):
    """Deterministic local embedding baseline for reproducible tests and demos."""

    def __init__(self, dimensions: int = 384) -> None:
        self.dimensions = dimensions

    def encode(self, texts: list[str]) -> np.ndarray:
        vectors = np.zeros((len(texts), self.dimensions), dtype=np.float32)
        for row, text in enumerate(texts):
            for token in TOKEN_RE.findall(text.lower()):
                digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
                bucket = int.from_bytes(digest[:4], "little") % self.dimensions
                sign = 1.0 if digest[4] % 2 == 0 else -1.0
                vectors[row, bucket] += sign
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / np.maximum(norms, 1e-12)


def build_embedding_model(backend: str) -> EmbeddingModel:
    if backend == "hashing":
        return HashingEmbeddingModel()
    if backend.startswith("sentence-transformers:"):
        model_name = backend.split(":", 1)[1]
        return SentenceTransformerEmbeddingModel(model_name)
    raise ValueError(f"Unsupported embedding backend: {backend}")


class SentenceTransformerEmbeddingModel(EmbeddingModel):
    def __init__(self, model_name: str) -> None:
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(model_name)

    def encode(self, texts: list[str]) -> np.ndarray:
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        return np.asarray(embeddings, dtype=np.float32)

