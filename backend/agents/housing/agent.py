"""
Scout Housing Agent.

Defines the specialist agent responsible for helping
students find temporary accommodation and safe housing.
"""

from google.adk.agents import Agent

from backend.agents.agent_builder import build_agent
from backend.agents.housing.constants import (
    AGENT_NAME,
    DESCRIPTION,
    PROMPT_FOLDER,
)
from backend.models import (
    HousingRecommendation,
)
from backend.tools import search_web


# ==========================================================
# Housing Agent Factory
# ==========================================================

def create_housing_agent() -> Agent:
    """
    Create and configure the Scout Housing Agent.
    """

    return build_agent(
        name=AGENT_NAME,
        prompt_folder=PROMPT_FOLDER,
        description=DESCRIPTION,
        tools=[
            search_web,
        ],
        output_schema=HousingRecommendation,
    )


__all__ = (
    "create_housing_agent",
)