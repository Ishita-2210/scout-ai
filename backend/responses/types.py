"""
Scout Response Types.

Defines normalized response types used throughout Scout.
"""

from enum import Enum


class ResponseType(str, Enum):
    """
    Supported response types.
    """

    TEXT = "text"
    STRUCTURED = "structured"
    ERROR = "error"
    TOOL = "tool"


__all__ = (
    "ResponseType",
)