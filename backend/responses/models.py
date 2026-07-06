"""
Scout Response Models.

Normalized response models shared across Scout.
"""

from typing import Any

from pydantic import Field

from backend.models.common import DomainModel
from backend.responses.types import ResponseType


class AgentResponse(DomainModel):
    """
    Normalized response returned by Scout.
    """

    response_type: ResponseType = Field(
        description="Response category.",
    )

    content: Any = Field(
        description="Normalized response content.",
    )

    source_agent: str | None = Field(
        default=None,
        description="Agent that produced the response.",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional response metadata.",
    )


__all__ = (
    "AgentResponse",
)