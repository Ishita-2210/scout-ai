"""
Scout Configuration Exceptions.
"""

from backend.exceptions.base import ScoutError


class ConfigurationError(
    ScoutError,
):
    """Configuration failure."""


class MissingEnvironmentVariableError(
    ConfigurationError,
):
    """Environment variable missing."""