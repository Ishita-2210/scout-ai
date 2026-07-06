"""
Constants for the Scout Root Agent.
"""

from typing import Final


# ==========================================================
# Agent Identity
# ==========================================================

AGENT_NAME: Final = "scout_root"

DESCRIPTION: Final = (
    "Primary conversational entry point for the "
    "Scout multi-agent system."
)


# ==========================================================
# Prompt Configuration
# ==========================================================

PROMPT_FOLDER: Final = "root"

SYSTEM_PROMPT: Final = "system.md"


# ==========================================================
# Agent Configuration
# ==========================================================

MODEL_TEMPERATURE: Final = 0.2

MAX_RETRIES: Final = 3