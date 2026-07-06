"""
Scout Semantic Document Chunker.

Splits source documents into semantic chunks
optimized for embedding and retrieval.
"""

from __future__ import annotations

import logging
import re
from hashlib import sha256

from backend.rag.models import (
    DocumentChunk,
    SourceDocument,
)

logger = logging.getLogger(__name__)


# ==========================================================
# Configuration
# ==========================================================


DEFAULT_CHUNK_SIZE = 1000

DEFAULT_OVERLAP = 150

MIN_CHUNK_SIZE = 200


# ==========================================================
# Semantic Chunker
# ==========================================================


class SemanticChunker:
    """
    Produces semantically meaningful chunks
    from source documents.
    """

    def __init__(
        self,
        *,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        overlap: int = DEFAULT_OVERLAP,
    ) -> None:

        self.chunk_size = chunk_size
        self.overlap = overlap

    # ------------------------------------------------------
    # Public API
    # ------------------------------------------------------

    def chunk_document(
        self,
        document: SourceDocument,
    ) -> list[DocumentChunk]:
        """
        Chunk a single document.
        """

        sections = self._split_sections(
            document.text,
        )

        chunks: list[DocumentChunk] = []

        index = 0

        for section in sections:

            chunks.extend(
                self._chunk_section(
                    document=document,
                    section=section,
                    start_index=index,
                )
            )

            index = len(chunks)

        logger.info(
            "Created %d chunks for '%s'.",
            len(chunks),
            document.title,
        )

        return chunks

    def chunk_documents(
        self,
        documents: list[SourceDocument],
    ) -> list[DocumentChunk]:
        """
        Chunk multiple documents.
        """

        chunks: list[DocumentChunk] = []

        for document in documents:

            chunks.extend(
                self.chunk_document(
                    document,
                )
            )

        return chunks
    # ------------------------------------------------------
    # Section Splitting
    # ------------------------------------------------------

    def _split_sections(
        self,
        text: str,
    ) -> list[str]:
        """
        Split a document into semantic sections.

        Sections are separated by one or more
        blank lines.
        """

        sections = [
            section.strip()
            for section in re.split(
                r"\n\s*\n+",
                text,
            )
            if section.strip()
        ]

        return sections

    # ------------------------------------------------------
    # Chunk Section
    # ------------------------------------------------------

    def _chunk_section(
        self,
        *,
        document: SourceDocument,
        section: str,
        start_index: int,
    ) -> list[DocumentChunk]:
        """
        Chunk a single semantic section.
        """

        if len(section) <= self.chunk_size:

            return [
                self._create_chunk(
                    document=document,
                    text=section,
                    index=start_index,
                )
            ]

        chunks: list[DocumentChunk] = []

        start = 0
        index = start_index

        while start < len(section):

            end = min(
                start + self.chunk_size,
                len(section),
            )

            if end < len(section):

                boundary = section.rfind(
                    " ",
                    start,
                    end,
                )

                if (
                    boundary != -1
                    and boundary - start >= MIN_CHUNK_SIZE
                ):
                    end = boundary

            chunk_text = section[start:end].strip()

            if chunk_text:

                chunks.append(
                    self._create_chunk(
                        document=document,
                        text=chunk_text,
                        index=index,
                    )
                )

                index += 1

            if end >= len(section):
                break

            start = max(
                end - self.overlap,
                0,
            )

        return chunks

    # ------------------------------------------------------
    # Chunk Factory
    # ------------------------------------------------------

    def _create_chunk(
        self,
        *,
        document: SourceDocument,
        text: str,
        index: int,
    ) -> DocumentChunk:
        """
        Create a deterministic chunk.
        """

        chunk_id = sha256(
            f"{document.id}:{index}:{text}".encode(
                "utf-8",
            )
        ).hexdigest()

        return DocumentChunk(
            id=chunk_id,
            document_id=document.id,
            text=text,
            index=index,
        )


semantic_chunker = SemanticChunker()


__all__ = (
    "SemanticChunker",
    "semantic_chunker",
)