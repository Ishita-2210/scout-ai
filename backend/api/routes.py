"""
Scout API Routes.

Defines all HTTP endpoints exposed by the Scout backend.
"""

from fastapi import APIRouter, HTTPException, status

from backend.execution.runner import ScoutRunner
from backend.schemas.chat import ChatRequest, ChatResponse


# ---------------------------------------------------------
# Router
# ---------------------------------------------------------

router = APIRouter(
    prefix="/api/v1",
    tags=["Scout"],
)


# ---------------------------------------------------------
# Runner (Singleton)
# ---------------------------------------------------------

runner = ScoutRunner()


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
)
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict:
            Service health information.
    """

    return {
        "status": "healthy",
        "service": "Scout AI",
    }


# ---------------------------------------------------------
# Chat Endpoint
# ---------------------------------------------------------

@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat with Scout",
)
async def chat(
    request: ChatRequest,
) -> ChatResponse:
    """
    Send a message to Scout.

    Parameters
    ----------
    request:
        Incoming chat request.

    Returns
    -------
    ChatResponse
        Assistant response.
    """

    try:

        assistant_message = await runner.chat(
            user_id=request.user_id,
            session_id=request.session_id,
            message=request.message,
        )

        return ChatResponse(
            message=assistant_message,
            user_id=request.user_id,
            session_id=request.session_id,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Scout execution failed: {str(exc)}",
        ) from exc