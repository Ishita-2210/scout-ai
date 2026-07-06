"""
Scout Legal Agent.

Defines the specialist agent responsible for helping
students understand educational rights, government
policies, and official legal procedures.
"""

from google.adk.agents import Agent

from backend.agents.agent_builder import build_agent
from backend.agents.legal.constants import (
    AGENT_NAME,
    DESCRIPTION,
    PROMPT_FOLDER,
)
from backend.models import (
    LegalRecommendation,
)
from backend.tools import search_web


# ==========================================================
# Legal Agent Factory
# ==========================================================

def create_legal_agent() -> Agent:
    """
    Create and configure the Scout Legal Agent.

    Returns
    -------
    Agent
        Configured Google ADK Legal Agent.
    """

    return build_agent(
        name=AGENT_NAME,
        prompt_folder=PROMPT_FOLDER,
        description=DESCRIPTION,
        tools=[
            search_web,
        ],
        output_schema=LegalRecommendation,
    )


__all__ = (
    "create_legal_agent",
)