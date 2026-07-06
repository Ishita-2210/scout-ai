"""
Scout Memory Models.

Defines the domain models used by the Scout
memory subsystem.
"""

from pydantic import Field

from backend.models.common import DomainModel


# ==========================================================
# User Profile
# ==========================================================


class UserProfile(DomainModel):
    """
    Persistent user profile maintained across
    conversations.
    """

    name: str | None = Field(
        default=None,
        description="User's preferred name.",
    )

    age: int | None = Field(
        default=None,
        ge=0,
        le=120,
        description="User's age.",
    )

    grade: str | None = Field(
        default=None,
        description="Current academic grade.",
    )

    location: str | None = Field(
        default=None,
        description="Current city, district, or location.",
    )

    school_type: str | None = Field(
        default=None,
        description="Preferred school type.",
    )

    education_board: str | None = Field(
        default=None,
        description="Educational board (CBSE, ICSE, State Board, etc.).",
    )

    preferred_language: str | None = Field(
        default=None,
        description="Preferred language for communication.",
    )


# ==========================================================
# Memory Update
# ==========================================================


class MemoryUpdate(DomainModel):
    """
    Partial update extracted from a conversation.

    Every field is optional so newly extracted
    information never overwrites existing values
    with None.
    """

    name: str | None = Field(
        default=None,
        description="User's preferred name.",
    )

    age: int | None = Field(
        default=None,
        ge=0,
        le=120,
        description="User's age.",
    )

    grade: str | None = Field(
        default=None,
        description="Current academic grade.",
    )

    location: str | None = Field(
        default=None,
        description="Current city, district, or location.",
    )

    school_type: str | None = Field(
        default=None,
        description="Preferred school type.",
    )

    education_board: str | None = Field(
        default=None,
        description="Educational board.",
    )

    preferred_language: str | None = Field(
        default=None,
        description="Preferred language for communication.",
    )


__all__ = (
    "UserProfile",
    "MemoryUpdate",
)