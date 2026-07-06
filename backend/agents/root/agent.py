"""
Scout Root Agent.

Defines the primary conversational
entry point for the Scout system.
"""

from __future__ import annotations

from google.adk.agents import Agent

from backend.agents.agent_builder import (
    build_agent,
)

from backend.agents.root.constants import (
    AGENT_NAME,
    DESCRIPTION,
    PROMPT_FOLDER,
)


# ==========================================================
# Root Agent Factory
# ==========================================================


def create_root_agent(
    *,
    sub_agents: list[Agent] | None = None,
) -> Agent:
    """
    Create the Scout Root Agent.

    The Root Agent serves as the single
    entry point into the Scout multi-agent
    system and delegates requests to the
    appropriate specialist agents.

    Parameters
    ----------
    sub_agents
        Specialist agents available for
        delegation.

    Returns
    -------
    Agent
        Configured Root Agent.
    """

    return build_agent(
        name=AGENT_NAME,
        prompt_folder=PROMPT_FOLDER,
        description=DESCRIPTION,
        sub_agents=sub_agents,
    )


__all__ = (
    "create_root_agent",
)