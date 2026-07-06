"""
Scout Housing Models.

Defines domain models related to temporary
housing and accommodation.
"""

from pydantic import Field

from backend.models.common import DomainModel


# ==========================================================
# Housing
# ==========================================================

class Housing(DomainModel):
    """
    Represents a temporary housing recommendation.
    """

    name: str = Field(
        description="Official name of the accommodation.",
    )

    accommodation_type: str | None = Field(
        default=None,
        description="Type of accommodation (hostel, shelter, relief camp, NGO, residential school, etc.).",
    )

    address: str = Field(
        description="Physical address.",
    )

    phone: str | None = Field(
        default=None,
        description="Primary contact number.",
    )

    website: str | None = Field(
        default=None,
        description="Official website.",
    )

    eligibility: str | None = Field(
        default=None,
        description="Eligibility criteria, if applicable.",
    )

    services: list[str] = Field(
        default_factory=list,
        description="Facilities or services provided.",
    )

    description: str | None = Field(
        default=None,
        description="Brief overview of the accommodation.",
    )

    notes: str | None = Field(
        default=None,
        description="Additional information or recommendations.",
    )


# ==========================================================
# Housing Recommendation
# ==========================================================

class HousingRecommendation(DomainModel):
    """
    Structured housing recommendations.
    """

    query: str = Field(
        description="Original user request.",
    )

    housing: list[Housing] = Field(
        default_factory=list,
        description="Recommended accommodation options.",
    )

    summary: str | None = Field(
        default=None,
        description="Brief summary of the recommendations.",
    )


__all__ = (
    "Housing",
    "HousingRecommendation",
)