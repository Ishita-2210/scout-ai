"""
Scout API Schemas.

Common API response models shared across endpoints.
"""

from pydantic import Field

from backend.models.common import DomainModel


class HealthResponse(DomainModel):
    """
    Health check response.
    """

    status: str = Field(
        description="Service status.",
    )

    service: str = Field(
        description="Service name.",
    )

    version: str = Field(
        description="Application version.",
    )


class ErrorResponse(DomainModel):
    """
    Standard API error response.
    """

    detail: str = Field(
        description="Human-readable error message.",
    )


__all__ = (
    "HealthResponse",
    "ErrorResponse",
)