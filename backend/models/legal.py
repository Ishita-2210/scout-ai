"""
Scout Legal Models.

Defines domain models related to educational rights,
government policies, and legal resources.
"""

from pydantic import Field

from backend.models.common import DomainModel


# ==========================================================
# Legal Resource
# ==========================================================

class LegalResource(DomainModel):
    """
    Represents a legal or governmental educational resource.
    """

    title: str = Field(
        description="Official title of the legal resource.",
    )

    authority: str | None = Field(
        default=None,
        description="Issuing authority or organization.",
    )

    category: str | None = Field(
        default=None,
        description="Type of legal resource (Act, Policy, Scheme, Guideline, Notification, etc.).",
    )

    summary: str | None = Field(
        default=None,
        description="Short explanation of the resource.",
    )

    eligibility: str | None = Field(
        default=None,
        description="Eligibility criteria, if applicable.",
    )

    official_url: str | None = Field(
        default=None,
        description="Official government or organizational website.",
    )

    notes: str | None = Field(
        default=None,
        description="Additional recommendations or important notes.",
    )


# ==========================================================
# Legal Recommendation
# ==========================================================

class LegalRecommendation(DomainModel):
    """
    Structured legal guidance for the user.
    """

    query: str = Field(
        description="Original user request.",
    )

    resources: list[LegalResource] = Field(
        default_factory=list,
        description="Relevant legal resources.",
    )

    summary: str | None = Field(
        default=None,
        description="Brief summary of the recommendations.",
    )


__all__ = (
    "LegalResource",
    "LegalRecommendation",
)