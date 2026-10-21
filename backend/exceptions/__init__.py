"""Scout exception types."""

from backend.exceptions.agent import AgentAlreadyRegisteredError, AgentError, AgentNotFoundError
from backend.exceptions.base import ScoutError
from backend.exceptions.configuration import ConfigurationError, MissingEnvironmentVariableError
from backend.exceptions.memory import MemoryError, MemoryExtractionError, MemoryStorageError
from backend.exceptions.runner import EmptyResponseError, RunnerError, SessionError
from backend.exceptions.search import SearchAPIError, SearchError, SearchTimeoutError

__all__ = (
    "AgentError",
    "AgentAlreadyRegisteredError",
    "AgentNotFoundError",
    "ScoutError",
    "ConfigurationError",
    "MissingEnvironmentVariableError",
    "MemoryError",
    "MemoryStorageError",
    "MemoryExtractionError",
    "RunnerError",
    "EmptyResponseError",
    "SessionError",
    "SearchError",
    "SearchTimeoutError",
    "SearchAPIError",
)
