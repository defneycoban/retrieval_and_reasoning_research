from app.core.schemas import DocumentInput, QueryInput
from app.rag.embeddings import HashingEmbeddingModel
from app.rag.pipeline import RagPipeline
from app.rag.reasoning import ContextualReasoner
from app.rag.vector_store import InMemoryVectorStore


def build_pipeline() -> RagPipeline:
    return RagPipeline(
        embedding_model=HashingEmbeddingModel(),
        vector_store=InMemoryVectorStore(),
        reasoner=ContextualReasoner(),
    )


def test_pipeline_retrieves_indexed_document() -> None:
    pipeline = build_pipeline()
    pipeline.ingest(
        DocumentInput(
            doc_id="tr-1",
            language="tr",
            title="Turkish morphology",
            text="Türkçe eklemeli bir dildir ve biçimbirimsel çeşitlilik önemlidir.",
        )
    )

    response = pipeline.query(
        QueryInput(query="Türkçe eklemeli dil", language="tr", top_k=1)
    )

    assert response.contexts
    assert response.contexts[0].doc_id == "tr-1"
    assert "retrieved context" in response.answer

