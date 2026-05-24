from typing import Optional

from pydantic import BaseModel, Field


class DocumentInput(BaseModel):
    doc_id: str = Field(..., examples=["tr_morphology_001"])
    text: str
    language: str = Field(..., examples=["tr", "en"])
    title: Optional[str] = None
    metadata: dict[str, str] = Field(default_factory=dict)


class QueryInput(BaseModel):
    query: str
    language: str = Field(..., examples=["en", "tr"])
    top_k: int = Field(default=3, ge=1, le=20)


class RetrievedChunk(BaseModel):
    doc_id: str
    chunk_id: str
    text: str
    language: str
    score: float
    title: Optional[str] = None
    metadata: dict[str, str] = Field(default_factory=dict)


class QueryResponse(BaseModel):
    query: str
    language: str
    answer: str
    contexts: list[RetrievedChunk]


class EvaluationCase(BaseModel):
    case_id: str
    query: str
    language: str
    relevant_doc_ids: list[str]
    notes: Optional[str] = None


class EvaluationRequest(BaseModel):
    cases: list[EvaluationCase]
    top_k: int = Field(default=5, ge=1, le=20)


class RetrievalMetrics(BaseModel):
    recall_at_k: float
    mean_reciprocal_rank: float
    cases_evaluated: int
