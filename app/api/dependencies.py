from functools import lru_cache

from app.core.config import get_settings
from app.rag.embeddings import build_embedding_model
from app.rag.pipeline import RagPipeline
from app.rag.reasoning import ContextualReasoner
from app.rag.vector_store import InMemoryVectorStore


@lru_cache
def get_pipeline() -> RagPipeline:
    settings = get_settings()
    return RagPipeline(
        embedding_model=build_embedding_model(settings.embedding_backend),
        vector_store=InMemoryVectorStore(),
        reasoner=ContextualReasoner(),
    )

