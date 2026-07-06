"""
Scout Authentication Schemas.
"""

from pydantic import EmailStr, Field

from backend.models.common import DomainModel


class LoginRequest(DomainModel):
    """
    Login request.
    """

    email: EmailStr = Field(
        description="User email address.",
    )

    password: str = Field(
        min_length=8,
        description="User password.",
    )


class TokenResponse(DomainModel):
    """
    Authentication token response.
    """

    access_token: str = Field(
        description="JWT access token.",
    )

    token_type: str = Field(
        default="Bearer",
        description="Token type.",
    )


__all__ = (
    "LoginRequest",
    "TokenResponse",
)