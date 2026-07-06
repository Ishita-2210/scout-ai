"""
Constants for the Scout School Agent.
"""

from typing import Final


# ==========================================================
# Agent Identity
# ==========================================================

AGENT_NAME: Final = "school_agent"

DESCRIPTION: Final = (
    "Specialized agent responsible for helping students "
    "find suitable schools, understand admissions, "
    "enrollment procedures, grade placement, and "
    "educational pathways."
)


# ==========================================================
# Prompt Configuration
# ==========================================================

PROMPT_FOLDER: Final = "school"

SYSTEM_PROMPT: Final = "system.md"


# ==========================================================
# Model Configuration
# ==========================================================

MODEL_TEMPERATURE: Final = 0.2

MAX_RETRIES: Final = 3


__all__ = (
    "AGENT_NAME",
    "DESCRIPTION",
    "PROMPT_FOLDER",
    "SYSTEM_PROMPT",
    "MODEL_TEMPERATURE",
    "MAX_RETRIES",
)