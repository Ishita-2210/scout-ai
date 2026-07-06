"""
Scout Counselling Agent.

Defines the specialist agent responsible for supporting
students through educational wellbeing, motivation,
study planning, and school re-engagement.
"""

from google.adk.agents import Agent

from backend.agents.agent_builder import build_agent

from backend.agents.counselling.constants import (
    AGENT_NAME,
    DESCRIPTION,
    PROMPT_FOLDER,
)

from backend.models import CounsellingResponse


# ==========================================================
# Counselling Agent Factory
# ==========================================================

def create_counselling_agent() -> Agent:
    """
    Create and configure the Scout Counselling Agent.

    Returns
    -------
    Agent
        Configured Google ADK Counselling Agent.
    """

    return build_agent(
        name=AGENT_NAME,
        prompt_folder=PROMPT_FOLDER,
        description=DESCRIPTION,
        output_schema=CounsellingResponse,
    )


__all__ = (
    "create_counselling_agent",
)