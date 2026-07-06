"""
Scout API Schemas.
"""

from backend.schemas.api import (
    ErrorResponse,
    HealthResponse,
)

from backend.schemas.auth import (
    LoginRequest,
    TokenResponse,
)

from backend.schemas.chat import (
    ChatRequest,
    ChatResponse,
)

__all__ = (
    "HealthResponse",
    "ErrorResponse",
    "LoginRequest",
    "TokenResponse",
    "ChatRequest",
    "ChatResponse",
)