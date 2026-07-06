"""
Scout Common Domain Models.

Shared base models used across Scout.
"""

from pydantic import BaseModel, ConfigDict


class DomainModel(BaseModel):
    """
    Base class for all Scout domain models.
    """

    model_config = ConfigDict(
        frozen=False,
        extra="forbid",
        validate_assignment=True,
        populate_by_name=True,
        str_strip_whitespace=True,
    )


__all__ = (
    "DomainModel",
)