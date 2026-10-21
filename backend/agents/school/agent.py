"""
Scout School Agent.

Defines the specialist agent responsible for helping
students reconnect with education.
"""

from __future__ import annotations

from backend.agents.agent_builder import (
    Agent,
    build_agent,
)
from backend.agents.school.constants import (
    AGENT_NAME,
    DESCRIPTION,
    PROMPT_FOLDER,
)
from backend.models.school import (
    SchoolRecommendation,
)
from backend.tools import (
    search_web,
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
        Configured Scout School Agent.
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


__all__ = ("create_school_agent",)
