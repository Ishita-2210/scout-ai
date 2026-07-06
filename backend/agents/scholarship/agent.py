"""
Scout Scholarship Agent.
"""

from google.adk.agents import Agent

from backend.agents.agent_builder import build_agent
from backend.agents.scholarship.constants import (
    AGENT_NAME,
    DESCRIPTION,
    PROMPT_FOLDER,
)
from backend.tools import search_web
from backend.models import (
    ScholarshipRecommendation,
)

def create_scholarship_agent() -> Agent:
    """
    Create the Scout Scholarship Agent.
    """

    return build_agent(
        name=AGENT_NAME,
        prompt_folder=PROMPT_FOLDER,
        description=DESCRIPTION,
        tools=[
            search_web,
        ],
        output_schema=ScholarshipRecommendation,
    )


__all__ = (
    "create_scholarship_agent",
)