"""
Constants for the Scout Counselling Agent.
"""

from typing import Final


# ==========================================================
# Agent Identity
# ==========================================================

AGENT_NAME: Final = "counselling_agent"

DESCRIPTION: Final = (
    "Specialized agent responsible for supporting displaced "
    "students through emotional wellbeing, educational "
    "motivation, resilience, and study planning."
)


# ==========================================================
# Prompt Configuration
# ==========================================================

PROMPT_FOLDER: Final = "counselling"

SYSTEM_PROMPT: Final = "system.md"


# ==========================================================
# Model Configuration
# ==========================================================

MODEL_TEMPERATURE: Final = 0.5

MAX_RETRIES: Final = 3