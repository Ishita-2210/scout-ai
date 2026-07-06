"""
Constants for the Scout Housing Agent.
"""

from typing import Final


# ==========================================================
# Agent Identity
# ==========================================================

AGENT_NAME: Final = "housing_agent"

DESCRIPTION: Final = (
    "Specialized agent responsible for helping displaced "
    "students and families find safe temporary housing, "
    "student hostels, shelters, and accommodation near schools."
)


# ==========================================================
# Prompt Configuration
# ==========================================================

PROMPT_FOLDER: Final = "housing"

SYSTEM_PROMPT: Final = "system.md"


# ==========================================================
# Model Configuration
# ==========================================================

MODEL_TEMPERATURE: Final = 0.2

MAX_RETRIES: Final = 3