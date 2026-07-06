"""
Scout Memory Store.

Provides in-memory storage for user profiles.
"""

from backend.memory.models import UserProfile


class MemoryStore:
    """
    In-memory user profile storage.
    """

    def __init__(self) -> None:

        self._profiles: dict[str, UserProfile] = {}

    def exists(
        self,
        user_id: str,
    ) -> bool:

        return user_id in self._profiles

    def get(
        self,
        user_id: str,
    ) -> UserProfile:

        return self._profiles.setdefault(
            user_id,
            UserProfile(),
        )

    def save(
        self,
        user_id: str,
        profile: UserProfile,
    ) -> None:

        self._profiles[user_id] = profile

    def delete(
        self,
        user_id: str,
    ) -> None:

        self._profiles.pop(
            user_id,
            None,
        )

    def clear(self) -> None:

        self._profiles.clear()


memory_store = MemoryStore()


__all__ = (
    "MemoryStore",
    "memory_store",
)