"""
Scout Memory Formatter.

Formats user memory into textual context that can
be injected into Scout agent conversations.
"""

from typing import Final

from backend.memory.models import UserProfile


# ==========================================================
# Constants
# ==========================================================

EMPTY_CONTEXT: Final = (
    "No known information is currently stored "
    "about the user."
)

FIELD_LABELS: Final[dict[str, str]] = {
    "name": "Name",
    "age": "Age",
    "grade": "Grade",
    "location": "Location",
    "school_type": "School Type",
    "education_board": "Education Board",
    "preferred_language": "Preferred Language",
}


# ==========================================================
# Memory Formatter
# ==========================================================

class MemoryFormatter:
    """
    Formats user profiles into LLM-readable context.
    """

    def format_context(
        self,
        profile: UserProfile,
    ) -> str:
        """
        Convert a user profile into conversational context.

        Parameters
        ----------
        profile:
            User profile.

        Returns
        -------
        str
            Formatted memory context.
        """

        profile_data = profile.model_dump(
            exclude_none=True,
            exclude_unset=True,
        )

        if not profile_data:
            return EMPTY_CONTEXT

        lines = []

        for field, value in profile_data.items():

            label = FIELD_LABELS.get(
                field,
                field.replace("_", " ").title(),
            )

            lines.append(
                f"- {label}: {value}"
            )

        return (
            "Known information about the user:\n\n"
            + "\n".join(lines)
        )


# ==========================================================
# Singleton
# ==========================================================

memory_formatter = MemoryFormatter()


__all__ = (
    "MemoryFormatter",
    "memory_formatter",
)