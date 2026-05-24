from app.core.schemas import DocumentInput, QueryInput, QueryResponse, RetrievedChunk
from app.rag.chunking import chunk_text
from app.rag.embeddings import EmbeddingModel
from app.rag.reasoning import ContextualReasoner
from app.rag.vector_store import InMemoryVectorStore


class RagPipeline:
    def __init__(
        self,
        embedding_model: EmbeddingModel,
        vector_store: InMemoryVectorStore,
        reasoner: ContextualReasoner,
    ) -> None:
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.reasoner = reasoner

    def ingest(self, document: DocumentInput) -> int:
        chunks = chunk_text(
            doc_id=document.doc_id,
            text=document.text,
            language=document.language,
            title=document.title,
            metadata=document.metadata,
        )
        vectors = self.embedding_model.encode([chunk.text for chunk in chunks])
        self.vector_store.add(chunks, vectors)
        return len(chunks)

    def query(self, request: QueryInput) -> QueryResponse:
        query_vector = self.embedding_model.encode([request.query])[0]
        raw_contexts = self.vector_store.search(query_vector, top_k=request.top_k)
        contexts = [
            RetrievedChunk(
                doc_id=item["doc_id"],
                chunk_id=item["chunk_id"],
                text=item["text"],
                language=item["language"],
                title=item["title"],
                metadata=item["metadata"] or {},
                score=item["score"],
            )
            for item in raw_contexts
        ]
        return QueryResponse(
            query=request.query,
            language=request.language,
            answer=self.reasoner.answer(request.query, contexts),
            contexts=contexts,
        )

