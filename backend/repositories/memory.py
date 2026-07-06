"""
Scout Memory Repository.

Provides the persistence interface for the
Scout memory subsystem.

The repository abstracts the underlying storage
implementation so the memory service remains
independent of databases or in-memory stores.
"""

from backend.memory.models import (
    UserProfile,
)
from backend.memory.store import (
    memory_store,
)


class MemoryRepository:
    """
    Repository responsible for persisting
    and retrieving user memory profiles.
    """

    # ======================================================
    # CRUD
    # ======================================================

    def exists(
        self,
        user_id: str,
    ) -> bool:
        """
        Check whether a profile exists.
        """

        return memory_store.exists(
            user_id,
        )

    def load(
        self,
        user_id: str,
    ) -> UserProfile:
        """
        Load a user's profile.
        """

        return memory_store.get(
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

        memory_store.save(
            user_id,
            profile,
        )

    def delete(
        self,
        user_id: str,
    ) -> None:
        """
        Delete a stored profile.
        """

        memory_store.delete(
            user_id,
        )

    def clear(self) -> None:
        """
        Remove every stored profile.

        Intended for testing.
        """

        memory_store.clear()


memory_repository = MemoryRepository()


__all__ = (
    "MemoryRepository",
    "memory_repository",
)