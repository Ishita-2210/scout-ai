"""
Scout Memory Service.

Provides the public interface for Scout's
memory subsystem.
"""

from backend.memory.formatter import memory_formatter
from backend.memory.models import (
    MemoryUpdate,
    UserProfile,
)
from backend.repositories.memory import (
    memory_repository,
)


class MemoryService:
    """
    Facade for the Scout memory subsystem.

    Coordinates memory persistence,
    formatting, and information extraction.
    """

    # ======================================================
    # Profile Operations
    # ======================================================

    def load(
        self,
        user_id: str,
    ) -> UserProfile:
        """
        Load a user's memory profile.
        """

        return memory_repository.load(
            user_id,
        )

    def save(
        self,
        user_id: str,
        profile: UserProfile,
    ) -> None:
        """
        Persist a user profile.
        """

        memory_repository.save(
            user_id,
            profile,
        )

    def reset(
        self,
        user_id: str,
    ) -> None:
        """
        Remove every stored memory
        associated with the user.
        """

        memory_repository.delete(
            user_id,
        )

    # ======================================================
    # Memory Updates
    # ======================================================

    def merge(
        self,
        user_id: str,
        update: MemoryUpdate,
    ) -> UserProfile:
        """
        Merge newly extracted information
        into an existing user profile.
        """

        profile = self.load(
            user_id,
        )

        merged_profile = profile.model_copy(
            update=update.model_dump(
                exclude_none=True,
            ),
        )

        self.save(
            user_id,
            merged_profile,
        )

        return merged_profile

    # ======================================================
    # Context Building
    # ======================================================

    def build_context(
        self,
        user_id: str,
    ) -> str:
        """
        Build conversational memory context.
        """

        profile = self.load(
            user_id,
        )

        return memory_formatter.format_context(
            profile,
        )


memory_service = MemoryService()


__all__ = (
    "MemoryService",
    "memory_service",
)
