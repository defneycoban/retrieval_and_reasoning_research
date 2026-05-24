from app.core.schemas import RetrievedChunk


class ContextualReasoner:
    def answer(self, query: str, contexts: list[RetrievedChunk]) -> str:
        if not contexts:
            return "I could not find relevant context in the indexed documents."

        evidence = " ".join(chunk.text for chunk in contexts[:2])
        return (
            "Based on the retrieved context, the strongest evidence points to: "
            f"{evidence[:700]}"
        )

