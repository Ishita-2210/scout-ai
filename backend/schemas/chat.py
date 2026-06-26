from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Incoming chat request.
    """

    user_id: str = Field(...)

    session_id: str = Field(...)

    message: str = Field(...)


class ChatResponse(BaseModel):
    """
    Response returned by Scout.
    """

    response: str

    user_id: str

    session_id: str