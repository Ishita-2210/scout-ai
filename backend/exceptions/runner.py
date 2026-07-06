"""
Scout Runner Exceptions.
"""

from backend.exceptions.base import ScoutError


class RunnerError(
    ScoutError,
):
    """Base runner exception."""


class EmptyResponseError(
    RunnerError,
):
    """Scout returned no response."""


class SessionError(
    RunnerError,
):
    """Session failure."""