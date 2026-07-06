"""
Scout API Routes.

Defines all HTTP endpoints exposed by the Scout backend.
"""

import logging

from fastapi import APIRouter, HTTPException, status

from backend.execution.provider import get_runner
from backend.schemas.chat import (
    ChatRequest,
    ChatResponse,
)


# ==========================================================
# Logger
# ==========================================================

logger = logging.getLogger(__name__)


# ==========================================================
# Router
# ==========================================================

router = APIRouter(
    prefix="/api/v1",
    tags=["Scout"],
)


# ==========================================================
# Health Check
# ==========================================================

@router.get(
    "/health",
    summary="Health Check",
    description="Returns the health status of the Scout backend.",
    status_code=status.HTTP_200_OK,
)
async def health_check():
    """
    Health check endpoint.
    """

    return {
        "status": "healthy",
        "service": "Scout AI",
        "version": "1.0.0",
    }


# ==========================================================
# Chat Endpoint
# ==========================================================

@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with Scout",
    description="Send a message to Scout and receive an AI-generated response.",
    status_code=status.HTTP_200_OK,
)
async def chat(
    request: ChatRequest,
) -> ChatResponse:
    """
    Process a user message through Scout.
    """

    logger.info(
        "Received chat request from user '%s'.",
        request.user_id,
    )

    try:

        runner = get_runner()

        assistant_message = await runner.chat(
            user_id=request.user_id,
            session_id=request.session_id,
            message=request.message,
        )

        logger.info(
            "Successfully processed request for '%s'.",
            request.user_id,
        )

        return ChatResponse(
            message=assistant_message,
            user_id=request.user_id,
            session_id=request.session_id,
        )

    except Exception as exc:

        logger.exception(
            "Scout execution failed."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )