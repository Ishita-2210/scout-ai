"""
Scout Memory Exceptions.
"""

from backend.exceptions.base import ScoutError


class MemoryError(
    ScoutError,
):
    """Base memory exception."""


class MemoryStorageError(
    MemoryError,
):
    """Memory persistence failed."""


class MemoryExtractionError(
    MemoryError,
):
    """Memory extraction failed."""