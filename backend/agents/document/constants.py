"""
Constants for the Scout Document Agent.
"""

from typing import Final


# ==========================================================
# Agent Identity
# ==========================================================

AGENT_NAME: Final = "document_agent"

DESCRIPTION: Final = (
    "Specialized agent responsible for helping students "
    "understand admission documents, required certificates, "
    "and document recovery procedures."
)


# ==========================================================
# Prompt Configuration
# ==========================================================

PROMPT_FOLDER: Final = "document"

SYSTEM_PROMPT: Final = "system.md"


# ==========================================================
# Model Configuration
# ==========================================================

MODEL_TEMPERATURE: Final = 0.2

MAX_RETRIES: Final = 3