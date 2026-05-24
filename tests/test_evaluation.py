from app.core.schemas import DocumentInput, EvaluationCase
from app.evaluation.retrieval import evaluate_retrieval
from app.rag.embeddings import HashingEmbeddingModel
from app.rag.pipeline import RagPipeline
from app.rag.reasoning import ContextualReasoner
from app.rag.vector_store import InMemoryVectorStore


def test_evaluate_retrieval_reports_recall_and_mrr() -> None:
    pipeline = RagPipeline(
        embedding_model=HashingEmbeddingModel(),
        vector_store=InMemoryVectorStore(),
        reasoner=ContextualReasoner(),
    )
    pipeline.ingest(
        DocumentInput(
            doc_id="doc-a",
            language="en",
            text="retrieval augmented generation uses retrieved context",
        )
    )

    metrics = evaluate_retrieval(
        pipeline,
        [
            EvaluationCase(
                case_id="case-a",
                query="retrieved context",
                language="en",
                relevant_doc_ids=["doc-a"],
            )
        ],
        top_k=1,
    )

    assert metrics.recall_at_k == 1.0
    assert metrics.mean_reciprocal_rank == 1.0
    assert metrics.cases_evaluated == 1

