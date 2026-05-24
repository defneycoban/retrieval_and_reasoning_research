from app.rag.chunking import chunk_text


def test_chunk_text_preserves_document_metadata() -> None:
    chunks = chunk_text(
        doc_id="doc-1",
        text="one two three four",
        language="en",
        title="Example",
        metadata={"source": "test"},
        max_words=2,
        overlap_words=0,
    )

    assert len(chunks) == 2
    assert chunks[0].doc_id == "doc-1"
    assert chunks[0].language == "en"
    assert chunks[0].title == "Example"
    assert chunks[0].metadata == {"source": "test"}

