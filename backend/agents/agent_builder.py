"""
Scout Agent Builder.

Provides a reusable factory for creating
Google ADK agents using Scout's
project conventions.
"""

from __future__ import annotations

from typing import Any
from typing import Final

from google.adk.agents import Agent

from backend.agents.loader import (
    load_prompt,
)

from backend.config import (
    GEMINI_MODEL,
)


# ==========================================================
# Defaults
# ==========================================================

DEFAULT_SYSTEM_PROMPT: Final = "system.md"


# ==========================================================
# Helpers
# ==========================================================


def _load_instruction(
    prompt_folder: str,
) -> str:
    """
    Load the system instruction for an agent.
    """

    return load_prompt(
        agent_name=prompt_folder,
        filename=DEFAULT_SYSTEM_PROMPT,
    )


# ==========================================================
# Agent Builder
# ==========================================================


def build_agent(
    *,
    name: str,
    prompt_folder: str,
    description: str,
    model: str = GEMINI_MODEL,
    sub_agents: list[Agent] | None = None,
    tools: list[Any] | None = None,
    output_schema: type | None = None,
) -> Agent:
    """
    Build and configure a Scout ADK agent.

    Parameters
    ----------
    name
        Unique agent identifier.

    prompt_folder
        Folder containing the system prompt.

    description
        Human-readable description.

    model
        Gemini model name.

    sub_agents
        Optional delegated agents.

    tools
        Optional ADK tools.

    output_schema
        Optional structured output schema.

    Returns
    -------
    Agent
        Configured Google ADK agent.
    """

    instruction = _load_instruction(
        prompt_folder,
    )

    kwargs: dict[str, Any] = {
        "name": name,
        "model": model,
        "description": description,
        "instruction": instruction,
    }

    # ------------------------------------------------------
    # Optional Configuration
    # ------------------------------------------------------

    if sub_agents:
        kwargs["sub_agents"] = sub_agents

    if tools:
        kwargs["tools"] = tools

    #if output_schema is not None:
        #kwargs["output_schema"] = output_schema

    # ------------------------------------------------------
    # Build Agent
    # ------------------------------------------------------

    agent = Agent(
        **kwargs,
    )

    return agent


__all__ = (
    "build_agent",
)