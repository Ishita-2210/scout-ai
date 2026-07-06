"""
Scout Document Loader.

Loads supported knowledge base documents
into Scout RAG.

Currently supported:

- PDF
"""

from __future__ import annotations

import logging
from pathlib import Path
from uuid import uuid4

import fitz  # PyMuPDF

from backend.rag.models import SourceDocument

logger = logging.getLogger(__name__)


# ==========================================================
# Document Loader
# ==========================================================


class DocumentLoader:
    """
    Loads documents from disk.

    Responsible only for reading files and
    extracting raw text.
    """

    SUPPORTED_EXTENSIONS = {
        ".pdf",
    }

    # ------------------------------------------------------
    # Public API
    # ------------------------------------------------------

    def load_directory(
        self,
        directory: Path,
    ) -> list[SourceDocument]:
        """
        Load every supported document inside
        a directory.
        """

        if not directory.exists():

            raise FileNotFoundError(
                f"Directory not found: {directory}"
            )

        documents: list[SourceDocument] = []

        for file in sorted(directory.rglob("*")):

            if (
                file.is_file()
                and file.suffix.lower()
                in self.SUPPORTED_EXTENSIONS
            ):

                documents.append(
                    self.load_document(
                        file,
                    )
                )

        logger.info(
            "Loaded %d documents.",
            len(documents),
        )

        return documents

    # ------------------------------------------------------
    # Single Document
    # ------------------------------------------------------

    def load_document(
        self,
        path: Path,
    ) -> SourceDocument:
        """
        Load a single document.
        """

        suffix = path.suffix.lower()

        if suffix == ".pdf":

            return self._load_pdf(
                path,
            )

        raise ValueError(
            f"Unsupported document type: {suffix}"
        )

    # ------------------------------------------------------
    # PDF
    # ------------------------------------------------------

    def _load_pdf(
        self,
        path: Path,
    ) -> SourceDocument:
        """
        Load a PDF using PyMuPDF.
        """

        document = fitz.open(path)

        pages: list[str] = []

        try:

            for page in document:

                text = page.get_text(
                    "text",
                )

                if text:

                    pages.append(
                        text.strip(),
                    )

        finally:

            document.close()

        return SourceDocument(
            id=str(uuid4()),
            title=path.stem,
            source=path,
            text="\n\n".join(
                pages,
            ),
        )


document_loader = DocumentLoader()


__all__ = (
    "DocumentLoader",
    "document_loader",
)