"""
Scout Counselling Models.
"""

from pydantic import Field

from backend.models.common import DomainModel


class CounsellingResponse(DomainModel):
    """
    Response returned by the Counselling Agent.
    """

    guidance: str = Field(
        description="Counselling guidance for the student.",
    )

    recommendations: list[str] = Field(
        default_factory=list,
        description="Recommended next steps.",
    )


__all__ = (
    "CounsellingResponse",
)