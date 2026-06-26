from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Incoming request from the client.
    """

    user_id: str = Field(
        ...,
        description="Unique user identifier",
    )

    session_id: str = Field(
        ...,
        description="Conversation session identifier",
    )

    message: str = Field(
        ...,
        description="User message",
    )


class ChatResponse(BaseModel):
    """
    Response returned by Scout.
    """

    message: str = Field(
        ...,
        description="Assistant response",
    )

    user_id: str

    session_id: str