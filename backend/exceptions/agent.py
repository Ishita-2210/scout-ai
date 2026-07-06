"""
Scout Agent Exceptions.
"""

from backend.exceptions.base import ScoutError


class AgentError(ScoutError):
    """
    Base exception for agent-related failures.
    """


class AgentAlreadyRegisteredError(AgentError):
    """
    Raised when attempting to register an agent twice.
    """


class AgentNotFoundError(AgentError):
    """
    Raised when an agent cannot be found.
    """


__all__ = (
    "AgentError",
    "AgentAlreadyRegisteredError",
    "AgentNotFoundError",
)