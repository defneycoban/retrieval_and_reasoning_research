from app.core.schemas import EvaluationCase, RetrievalMetrics
from app.rag.pipeline import RagPipeline
from app.core.schemas import QueryInput


def evaluate_retrieval(
    pipeline: RagPipeline,
    cases: list[EvaluationCase],
    top_k: int,
) -> RetrievalMetrics:
    if not cases:
        return RetrievalMetrics(recall_at_k=0.0, mean_reciprocal_rank=0.0, cases_evaluated=0)

    recall_hits = 0
    reciprocal_ranks: list[float] = []

    for case in cases:
        response = pipeline.query(
            QueryInput(query=case.query, language=case.language, top_k=top_k)
        )
        retrieved_doc_ids = [context.doc_id for context in response.contexts]
        relevant = set(case.relevant_doc_ids)

        if relevant.intersection(retrieved_doc_ids):
            recall_hits += 1

        rank = 0.0
        for index, doc_id in enumerate(retrieved_doc_ids, start=1):
            if doc_id in relevant:
                rank = 1.0 / index
                break
        reciprocal_ranks.append(rank)

    return RetrievalMetrics(
        recall_at_k=recall_hits / len(cases),
        mean_reciprocal_rank=sum(reciprocal_ranks) / len(reciprocal_ranks),
        cases_evaluated=len(cases),
    )

