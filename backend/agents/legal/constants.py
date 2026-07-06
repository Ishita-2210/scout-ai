"""
Constants for the Scout Legal Agent.
"""

from typing import Final


# ==========================================================
# Agent Identity
# ==========================================================

AGENT_NAME: Final = "legal_agent"

DESCRIPTION: Final = (
    "Specialized agent responsible for helping students "
    "understand educational rights, government policies, "
    "legal procedures, and official regulations."
)


# ==========================================================
# Prompt Configuration
# ==========================================================

PROMPT_FOLDER: Final = "legal"

SYSTEM_PROMPT: Final = "system.md"


# ==========================================================
# Model Configuration
# ==========================================================

MODEL_TEMPERATURE: Final = 0.1

MAX_RETRIES: Final = 3