"""
Scout Knowledge Base Indexer.

Indexes all documents into the persistent
Chroma vector database.
"""

from __future__ import annotations

import logging
from pathlib import Path

from backend.rag.service import (
    rag_service,
)

logger = logging.getLogger(__name__)

# ==========================================================
# Knowledge Directory
# ==========================================================

KNOWLEDGE_DIRECTORY = (
    Path(__file__)
    .parent.parent
    / "knowledge"
)


# ==========================================================
# Index Knowledge Base
# ==========================================================

def build_knowledge_base() -> None:
    """
    Build the Scout knowledge base.
    """

    logger.info(
        "Indexing Scout knowledge base..."
    )

    indexed = rag_service.index_directory(
        KNOWLEDGE_DIRECTORY,
    )

    logger.info(
        "Successfully indexed %d chunks.",
        indexed,
    )

    print(
        "\n"
        "=====================================\n"
        " Scout Knowledge Base Ready\n"
        "=====================================\n"
        f" Indexed Chunks : {indexed}\n"
        f" Total Chunks   : {rag_service.count()}\n"
    )


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    build_knowledge_base()