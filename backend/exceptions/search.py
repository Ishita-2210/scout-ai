"""
Scout Search Exceptions.
"""

from backend.exceptions.base import ScoutError


class SearchError(
    ScoutError,
):
    """Base search exception."""


class SearchTimeoutError(
    SearchError,
):
    """Search timed out."""


class SearchAPIError(
    SearchError,
):
    """Search provider returned an error."""