"""
Scout Semantic Retriever.

Retrieves the most relevant knowledge
chunks from the Scout knowledge base.
"""

from __future__ import annotations

import logging

from backend.rag.chroma_store import (
    chroma_store,
)

from backend.rag.models import (
    RetrievedChunk,
)

logger = logging.getLogger(__name__)


# ==========================================================
# Retriever
# ==========================================================


class SemanticRetriever:
    """
    Performs semantic retrieval over
    the Scout knowledge base.
    """

    def __init__(
        self,
        *,
        default_limit: int = 5,
    ) -> None:

        self.default_limit = default_limit

    # ------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------

    def retrieve(
        self,
        query: str,
        *,
        limit: int | None = None,
    ) -> list[RetrievedChunk]:
        """
        Retrieve the most relevant chunks.
        """

        results = chroma_store.search(
            query=query,
            limit=limit or self.default_limit,
        )

        logger.info(
            "Retrieved %d chunks for query.",
            len(results),
        )

        return results
    # ------------------------------------------------------
    # Context Building
    # ------------------------------------------------------

    def build_context(
        self,
        query: str,
        *,
        limit: int | None = None,
        minimum_score: float = 0.30,
    ) -> str:
        """
        Build formatted retrieval context for the LLM.
        """

        retrieved = self.retrieve(
            query=query,
            limit=limit,
        )

        if not retrieved:

            logger.info(
                "No retrieval results found.",
            )

            return ""

        context: list[str] = []

        seen: set[str] = set()

        for result in retrieved:

            if result.score < minimum_score:
                continue

            text = result.chunk.text.strip()

            if not text:
                continue

            if text in seen:
                continue

            seen.add(text)

            context.append(
                text,
            )

        logger.info(
            "Prepared %d context chunks.",
            len(context),
        )

        return "\n\n".join(context)

    # ------------------------------------------------------
    # Availability
    # ------------------------------------------------------

    def has_context(
        self,
        query: str,
    ) -> bool:
        """
        Determine whether relevant knowledge
        exists for a query.
        """

        return bool(
            self.retrieve(
                query=query,
                limit=1,
            )
        )


# ==========================================================
# Singleton
# ==========================================================

semantic_retriever = SemanticRetriever()


__all__ = (
    "SemanticRetriever",
    "semantic_retriever",
)
