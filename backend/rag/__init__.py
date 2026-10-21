"""Optional semantic retrieval utilities; imports do not initialize a remote provider."""

from backend.rag.models import DocumentChunk, RetrievedChunk, SourceDocument

__all__ = ("SourceDocument", "DocumentChunk", "RetrievedChunk", "RAGService")


def __getattr__(name):
    if name == "RAGService":
        from backend.rag.service import RAGService

        return RAGService
    raise AttributeError(name)
