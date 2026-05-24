from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class TextChunk:
    doc_id: str
    chunk_id: str
    text: str
    language: str
    title: Optional[str] = None
    metadata: Optional[dict[str, str]] = None


def chunk_text(
    doc_id: str,
    text: str,
    language: str,
    title: Optional[str] = None,
    metadata: Optional[dict[str, str]] = None,
    max_words: int = 120,
    overlap_words: int = 20,
) -> list[TextChunk]:
    words = text.split()
    if not words:
        return []

    chunks: list[TextChunk] = []
    step = max(1, max_words - overlap_words)
    for index, start in enumerate(range(0, len(words), step)):
        window = words[start : start + max_words]
        if not window:
            continue
        chunks.append(
            TextChunk(
                doc_id=doc_id,
                chunk_id=f"{doc_id}:{index}",
                text=" ".join(window),
                language=language,
                title=title,
                metadata=metadata or {},
            )
        )
        if start + max_words >= len(words):
            break
    return chunks
