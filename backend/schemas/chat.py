"""
Scout Chat Schemas.
"""

from pydantic import Field

from backend.models.common import DomainModel


class ChatRequest(DomainModel):
    """
    Incoming chat request.
    """

    user_id: str = Field(
        description="Unique user identifier.",
    )

    session_id: str = Field(
        description="Conversation session identifier.",
    )

    message: str = Field(
        min_length=1,
        description="User message.",
    )


class ChatResponse(DomainModel):
    """
    Chat response.
    """

    message: str = Field(
        description="Assistant response.",
    )

    user_id: str = Field(
        description="User identifier.",
    )

    session_id: str = Field(
        description="Conversation session identifier.",
    )


__all__ = (
    "ChatRequest",
    "ChatResponse",
)