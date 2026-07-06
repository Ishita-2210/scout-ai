"""
Scout Embedding Service.

Provides vector embeddings for documents and
queries used by the Scout RAG pipeline.
"""

from __future__ import annotations

import logging
from typing import Protocol

from google import genai

from backend.config import GOOGLE_API_KEY

logger = logging.getLogger(__name__)

EMBEDDING_MODEL = "gemini-embedding-001"


# ==========================================================
# Embedding Provider Interface
# ==========================================================


class EmbeddingProvider(Protocol):
    """
    Interface implemented by every embedding provider.
    """

    def embed(
        self,
        text: str,
    ) -> list[float]:
        ...

    def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        ...


# ==========================================================
# Google Embedding Provider
# ==========================================================


class GoogleEmbeddingProvider:
    """
    Google Generative AI embedding provider.
    """

    def __init__(self) -> None:

        self.client = genai.Client(
            api_key=GOOGLE_API_KEY,
        )

    # ------------------------------------------------------
    # Single Embedding
    # ------------------------------------------------------

    def embed(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a single text.
        """

        response = self.client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text,
        )

        return response.embeddings[0].values

    # ------------------------------------------------------
    # Batch Embeddings
    # ------------------------------------------------------

    def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """

        embeddings: list[list[float]] = []

        for text in texts:

            embeddings.append(
                self.embed(
                    text,
                )
            )

        logger.info(
            "Generated %d embeddings.",
            len(embeddings),
        )

        return embeddings


# ==========================================================
# Singleton
# ==========================================================

embedding_provider = GoogleEmbeddingProvider()


__all__ = (
    "EmbeddingProvider",
    "GoogleEmbeddingProvider",
    "embedding_provider",
)