"""
Scout Chroma Vector Store.

Persistent vector database implementation
using ChromaDB.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Final

import chromadb
from chromadb.api.models.Collection import Collection

from backend.rag.models import (
    DocumentChunk,
    RetrievedChunk,
)
from backend.rag.embeddings import (
    embedding_provider,
)

logger = logging.getLogger(__name__)

# ==========================================================
# Configuration
# ==========================================================

DATABASE_PATH: Final = (
    Path("backend")
    / "data"
    / "chroma"
)

COLLECTION_NAME: Final = "scout_knowledge"


# ==========================================================
# Chroma Store
# ==========================================================


class ChromaStore:
    """
    Persistent Chroma vector database.
    """

    def __init__(
        self,
        *,
        database_path: Path = DATABASE_PATH,
        collection_name: str = COLLECTION_NAME,
    ) -> None:

        database_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = chromadb.PersistentClient(
            path=str(database_path),
        )

        self.collection: Collection = (
            self.client.get_or_create_collection(
                name=collection_name,
                metadata={
                    "description": (
                        "Scout RAG Knowledge Base"
                    ),
                },
            )
        )

        logger.info(
            "Initialized Chroma collection '%s'.",
            collection_name,
        )

    # ------------------------------------------------------
    # Indexing
    # ------------------------------------------------------

    def index_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> int:
        """
        Index document chunks.
        """

        if not chunks:

            return 0

        ids: list[str] = []
        documents: list[str] = []
        embeddings: list[list[float]] = []
        metadatas: list[dict] = []

        for chunk in chunks:

            ids.append(
                chunk.id,
            )

            documents.append(
                chunk.text,
            )

            embeddings.append(
                embedding_provider.embed(
                    chunk.text,
                )
            )

            metadata = {
                "document_id": chunk.document_id,
                "chunk_index": chunk.index,
            }

            if hasattr(
                chunk,
                "metadata",
            ):

                metadata.update(
                    chunk.metadata,
                )

            metadatas.append(
                metadata,
            )

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        logger.info(
            "Indexed %d chunks.",
            len(chunks),
        )

        return len(chunks)

    # ------------------------------------------------------
    # Search
    # ------------------------------------------------------

    def search(
        self,
        query: str,
        *,
        limit: int = 5,
    ) -> list[RetrievedChunk]:
        """
        Perform semantic similarity search.
        """

        query_embedding = embedding_provider.embed(
            query,
        )

        results = self.collection.query(
            query_embeddings=[
                query_embedding,
            ],
            n_results=limit,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        retrieved: list[RetrievedChunk] = []

        ids = results.get("ids", [[]])[0]
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for idx in range(len(ids)):

            metadata = metas[idx] or {}

            chunk = DocumentChunk(
                id=ids[idx],
                document_id=metadata.get(
                    "document_id",
                    "",
                ),
                text=docs[idx],
                index=metadata.get(
                    "chunk_index",
                    0,
                ),
                metadata={
                    k: v
                    for k, v in metadata.items()
                    if k
                    not in {
                        "document_id",
                        "chunk_index",
                    }
                },
            )

            distance = distances[idx]

            score = max(
                0.0,
                1.0 - float(distance),
            )

            retrieved.append(
                RetrievedChunk(
                    chunk=chunk,
                    score=score,
                    document=docs[idx],
                )
            )

        logger.info(
            "Retrieved %d chunks.",
            len(retrieved),
        )

        return retrieved

    # ------------------------------------------------------
    # Delete
    # ------------------------------------------------------

    def delete_document(
        self,
        document_id: str,
    ) -> None:
        """
        Delete every chunk belonging to a document.
        """

        self.collection.delete(
            where={
                "document_id": document_id,
            },
        )

        logger.info(
            "Deleted '%s'.",
            document_id,
        )

    # ------------------------------------------------------
    # Utilities
    # ------------------------------------------------------

    def count(
        self,
    ) -> int:
        """
        Number of indexed chunks.
        """

        return self.collection.count()

    def reset(
        self,
    ) -> None:
        """
        Remove every indexed chunk.
        """

        self.client.delete_collection(
            COLLECTION_NAME,
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=COLLECTION_NAME,
            )
        )

        logger.warning(
            "Knowledge base cleared.",
        )


# ==========================================================
# Singleton
# ==========================================================

chroma_store = ChromaStore()


__all__ = (
    "ChromaStore",
    "chroma_store",
)