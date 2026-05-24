from fastapi import APIRouter, Depends
from typing import Union

from app.api.dependencies import get_pipeline
from app.core.schemas import (
    DocumentInput,
    EvaluationRequest,
    QueryInput,
    QueryResponse,
    RetrievalMetrics,
)
from app.evaluation.retrieval import evaluate_retrieval
from app.experiments.tokenization import tokenization_profile
from app.rag.pipeline import RagPipeline

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/documents")
def ingest_document(
    document: DocumentInput,
    pipeline: RagPipeline = Depends(get_pipeline),
) -> dict[str, Union[int, str]]:
    chunk_count = pipeline.ingest(document)
    return {"doc_id": document.doc_id, "chunks_indexed": chunk_count}


@router.post("/query", response_model=QueryResponse)
def query(
    request: QueryInput,
    pipeline: RagPipeline = Depends(get_pipeline),
) -> QueryResponse:
    return pipeline.query(request)


@router.post("/evaluate/retrieval", response_model=RetrievalMetrics)
def evaluate(
    request: EvaluationRequest,
    pipeline: RagPipeline = Depends(get_pipeline),
) -> RetrievalMetrics:
    return evaluate_retrieval(pipeline, request.cases, request.top_k)


@router.post("/experiments/tokenization")
def analyze_tokenization(payload: dict[str, str]) -> dict:
    return tokenization_profile(payload.get("text", ""))
