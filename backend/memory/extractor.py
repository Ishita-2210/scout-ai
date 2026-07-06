"""
Scout Memory Extractor.

Extracts structured user information from
natural language conversations.
"""

from abc import ABC, abstractmethod

from backend.memory.models import MemoryUpdate


class BaseMemoryExtractor(ABC):
    """
    Base class for all memory extractors.
    """

    @abstractmethod
    def extract(
        self,
        message: str,
    ) -> MemoryUpdate:
        """
        Extract structured information from a message.
        """


class NullMemoryExtractor(BaseMemoryExtractor):
    """
    Placeholder implementation.

    Will later be replaced by an LLM-powered extractor.
    """

    def extract(
        self,
        message: str,
    ) -> MemoryUpdate:

        return MemoryUpdate()


memory_extractor = NullMemoryExtractor()


__all__ = (
    "BaseMemoryExtractor",
    "NullMemoryExtractor",
    "memory_extractor",
)