"""
Scout Base Exceptions.

Defines the common exception hierarchy used
throughout Scout.
"""

from typing import Any


class ScoutError(Exception):
    """
    Base exception for all Scout errors.
    """

    def __init__(
        self,
        message: str,
        *,
        error_code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(message)

        self.message = message
        self.error_code = error_code
        self.details = details or {}

    def __str__(self) -> str:

        if self.error_code:

            return (
                f"[{self.error_code}] "
                f"{self.message}"
            )

        return self.message