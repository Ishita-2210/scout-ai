"""
Scout Chat API.

Provides the REST API for interacting
with the Scout assistant.
"""

from __future__ import annotations
import json
import logging
from typing import Any

from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import Field

from backend.execution.runner import ScoutRunner

logger = logging.getLogger(__name__)
router = APIRouter()



# ==========================================================
# Request / Response Models
# ==========================================================


class ChatRequest(BaseModel):
    """
    Chat request payload.
    """

    user_id: str = Field(
        min_length=1,
        description="Unique user identifier.",
    )

    session_id: str = Field(
        min_length=1,
        description="Conversation session identifier.",
    )

    message: str = Field(
        min_length=1,
        description="User message.",
    )


class ChatResponse(BaseModel):
    """
    Chat response payload.
    """

    response: Any

# ==========================================================
# Chat Endpoint
# ==========================================================


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with Scout",
)
async def chat(
    request: ChatRequest,
) -> ChatResponse:
    """
    Execute a conversation turn with Scout.
    """

    logger.info(
        "Received chat request from user '%s'.",
        request.user_id,
    )
    runner = ScoutRunner()
    try:

        response = await runner.chat(
            user_id=request.user_id,
            session_id=request.session_id,
            message=request.message,
        )

    except ValueError as exc:

        logger.warning(
            "Invalid request: %s",
            exc,
        )

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:

        logger.exception(
            "Runner execution failed.",
        )

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    except Exception:

        logger.exception(
            "Unexpected server error.",
        )

        raise HTTPException(
            status_code=500,
            detail="Internal server error.",
        )

    logger.info(
        "Completed request for user '%s'.",
        request.user_id,
    )
    try:
        response = json.loads(response)
    except json.JSONDecodeError:
        pass
    
    return ChatResponse(
        response=response,
    )


__all__ = (
    "router",
)