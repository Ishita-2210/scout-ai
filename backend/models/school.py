"""
Scout School Models.

Defines domain models related to schools and
school recommendations.
"""

from pydantic import Field

from backend.models.common import DomainModel


# ==========================================================
# Address
# ==========================================================

class Address(DomainModel):
    """
    Physical address of a school.
    """

    street: str | None = Field(
        default=None,
        description="Street address.",
    )

    city: str | None = Field(
        default=None,
        description="City.",
    )

    state: str | None = Field(
        default=None,
        description="State or province.",
    )

    postal_code: str | None = Field(
        default=None,
        description="Postal or ZIP code.",
    )

    country: str | None = Field(
        default=None,
        description="Country.",
    )


# ==========================================================
# School
# ==========================================================

class School(DomainModel):
    """
    Represents a school.
    """

    name: str = Field(
        description="Official school name.",
    )

    address: Address = Field(
        default_factory=Address,
        description="School address.",
    )

    website: str | None = Field(
        default=None,
        description="Official website.",
    )

    phone: str | None = Field(
        default=None,
        description="Contact phone number.",
    )

    email: str | None = Field(
        default=None,
        description="Contact email address.",
    )

    board: str | None = Field(
        default=None,
        description="Educational board.",
    )

    school_type: str | None = Field(
        default=None,
        description="Government, private, aided, etc.",
    )

    grades: list[str] = Field(
        default_factory=list,
        description="Grades offered.",
    )

    description: str | None = Field(
        default=None,
        description="Short school description.",
    )


# ==========================================================
# School Recommendation
# ==========================================================

class SchoolRecommendation(DomainModel):
    """
    Recommendation returned by Scout.
    """

    query: str = Field(
        description="Original user query.",
    )

    schools: list[School] = Field(
        default_factory=list,
        description="Recommended schools.",
    )


__all__ = (
    "Address",
    "School",
    "SchoolRecommendation",
)