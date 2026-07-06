"""
Scout RAG Domain Models.

Defines immutable domain models used throughout
the retrieval pipeline.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import Field

from backend.models.common import DomainModel


# ==========================================================
# Source Document
# ==========================================================


class SourceDocument(DomainModel):
    """
    Represents a loaded source document.
    """

    id: str = Field(
        description="Unique document identifier.",
    )

    title: str = Field(
        description="Human-readable document title.",
    )

    source: Path = Field(
        description="Original document path.",
    )

    text: str = Field(
        description="Complete extracted document text.",
    )


# ==========================================================
# Document Chunk
# ==========================================================


class DocumentChunk(DomainModel):
    """
    Represents a semantic chunk generated
    from a source document.
    """

    id: str = Field(
        description="Unique chunk identifier.",
    )

    document_id: str = Field(
        description="Parent document identifier.",
    )

    text: str = Field(
        description="Chunk text.",
    )

    index: int = Field(
        ge=0,
        description="Chunk position inside the document.",
    )


# ==========================================================
# Retrieved Chunk
# ==========================================================


class RetrievedChunk(DomainModel):
    """
    Represents a retrieved semantic result.
    """

    chunk: DocumentChunk
    score: float
    content: str
    metadata: dict[str, str] = Field(
        default_factory=dict,
        description="Chunk metadata used for filtering and retrieval.",
    )
    score: float = Field(
        ge=0.0,
        le=1.0,
        description="Similarity score.",
    )


__all__ = (
    "SourceDocument",
    "DocumentChunk",
    "RetrievedChunk",
)