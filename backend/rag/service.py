"""
Scout Retrieval-Augmented Generation Service.

High-level orchestration layer for Scout's
Retrieval-Augmented Generation (RAG) pipeline.

This module coordinates document loading,
chunking, indexing, and semantic retrieval.

Agents should interact ONLY with this service.
"""

from __future__ import annotations

import logging
from pathlib import Path

from backend.rag.loader import (
    document_loader,
)

from backend.rag.chunker import (
    semantic_chunker,
)

from backend.rag.chroma_store import (
    chroma_store,
)

from backend.rag.retriever import (
    semantic_retriever,
)

logger = logging.getLogger(__name__)


# ==========================================================
# RAG Service
# ==========================================================


class RAGService:
    """
    High-level orchestration layer
    for the Scout RAG pipeline.
    """

    # ------------------------------------------------------
    # Knowledge Base Indexing
    # ------------------------------------------------------

    def index_directory(
        self,
        directory: Path,
    ) -> int:
        """
        Index every supported document
        inside a directory.

        Returns
        -------
        int
            Number of indexed chunks.
        """

        logger.info(
            "Loading knowledge base from '%s'.",
            directory,
        )

        documents = document_loader.load_directory(
            directory,
        )

        chunks = semantic_chunker.chunk_documents(
            documents,
        )

        indexed = chroma_store.index_chunks(
            chunks,
        )

        logger.info(
            "Indexed %d chunks.",
            indexed,
        )

        return indexed

    # ------------------------------------------------------
    # Single Document
    # ------------------------------------------------------

    def index_document(
        self,
        path: Path,
    ) -> int:
        """
        Index a single document.
        """

        document = document_loader.load_document(
            path,
        )

        chunks = semantic_chunker.chunk_document(
            document,
        )

        return chroma_store.index_chunks(
            chunks,
        )

    # ------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------

    def retrieve(
        self,
        query: str,
        *,
        limit: int = 5,
    ):
        """
        Retrieve the most relevant knowledge chunks.
        """

        return semantic_retriever.retrieve(
            query=query,
            limit=limit,
        )

    def retrieve_context(
        self,
        query: str,
        *,
        limit: int = 5,
        minimum_score: float = 0.30,
    ) -> str:
        """
        Retrieve formatted context suitable
        for LLM prompting.
        """

        return semantic_retriever.build_context(
            query=query,
            limit=limit,
            minimum_score=minimum_score,
        )

    # ------------------------------------------------------
    # Knowledge Base Information
    # ------------------------------------------------------

    def count(
        self,
    ) -> int:
        """
        Return the number of indexed chunks.
        """

        return chroma_store.count()

    def reset(
        self,
    ) -> None:
        """
        Clear the complete knowledge base.
        """

        logger.warning(
            "Resetting Scout knowledge base."
        )

        chroma_store.reset()

    def has_knowledge(
        self,
        query: str,
    ) -> bool:
        """
        Determine whether relevant knowledge
        exists for a query.
        """

        return semantic_retriever.has_context(
            query=query,
        )


# ==========================================================
# Singleton
# ==========================================================

rag_service = RAGService()


__all__ = (
    "RAGService",
    "rag_service",
)