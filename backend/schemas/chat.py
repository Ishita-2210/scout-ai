"""One request/response contract for the browser and API."""

from uuid import UUID

from pydantic import Field

from backend.config import MAX_MESSAGE_LENGTH
from backend.models.common import DomainModel
from backend.schemas.assistant import AssistantResult


class ChatRequest(DomainModel):
    session_id: UUID
    request_id: UUID
    message: str = Field(min_length=1, max_length=MAX_MESSAGE_LENGTH)


class ChatResponse(DomainModel):
    response: AssistantResult
    request_id: str
