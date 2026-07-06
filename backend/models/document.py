"""
Scout Document Models.

Defines domain models related to educational
documents required for school admissions.
"""

from pydantic import Field

from backend.models.common import DomainModel


# ==========================================================
# Document
# ==========================================================

class Document(DomainModel):
    """
    Represents a document that may be required
    during the admission process.
    """

    name: str = Field(
        description="Official document name.",
    )

    required: bool = Field(
        default=True,
        description="Whether the document is mandatory.",
    )

    available: bool | None = Field(
        default=None,
        description="Whether the student currently possesses the document.",
    )

    reason: str | None = Field(
        default=None,
        description="Reason why this document is required.",
    )

    issuing_authority: str | None = Field(
        default=None,
        description="Government office or authority responsible for issuing the document.",
    )

    replacement_available: bool | None = Field(
        default=None,
        description="Whether a duplicate or replacement can be obtained.",
    )

    replacement_process: str | None = Field(
        default=None,
        description="Brief description of the replacement procedure.",
    )

    official_url: str | None = Field(
        default=None,
        description="Official website for obtaining or replacing the document.",
    )

    notes: str | None = Field(
        default=None,
        description="Additional guidance or important notes.",
    )


# ==========================================================
# Document Checklist
# ==========================================================

class DocumentChecklist(DomainModel):
    """
    Structured checklist of admission documents.
    """

    query: str = Field(
        description="Original user request.",
    )

    documents: list[Document] = Field(
        default_factory=list,
        description="Documents relevant to the user's situation.",
    )

    summary: str | None = Field(
        default=None,
        description="Brief overview of the checklist.",
    )


__all__ = (
    "Document",
    "DocumentChecklist",
)