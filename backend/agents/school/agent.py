"""
Scout School Agent.

Defines the specialist agent responsible for helping
students reconnect with education.
"""

from __future__ import annotations

from google.adk.agents import Agent

from backend.agents.agent_builder import (
    build_agent,
)

from backend.agents.school.constants import (
    AGENT_NAME,
    DESCRIPTION,
    PROMPT_FOLDER,
)

from backend.tools import (
    search_web,
)

from backend.models.school import (
    SchoolRecommendation,
)


# ==========================================================
# School Agent Factory
# ==========================================================


def create_school_agent() -> Agent:
    """
    Create and configure the Scout School Agent.

    Returns
    -------
    Agent
        Configured Google ADK School Agent.
    """

    return build_agent(
        name=AGENT_NAME,
        prompt_folder=PROMPT_FOLDER,
        description=DESCRIPTION,
        tools=[
            search_web,
        ],
        output_schema=SchoolRecommendation,
    )


__all__ = (
    "create_school_agent",
)