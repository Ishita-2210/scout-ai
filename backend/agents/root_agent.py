"""
Root Scout Agent.

Defines the primary conversational agent for Scout.
"""

from google.adk.agents import Agent
from backend import config
from backend.agents.loader import load_prompt


def create_root_agent() -> Agent:
    """
    Create and return the Scout Root Agent.
    """

    instruction = load_prompt(
        "root",
        "system.md",
    )

    return Agent(
        name="scout_root",
        model="gemini-2.5-flash",
        description="Primary entry point for Scout.",
        instruction=instruction,
    )


__all__ = [
    "create_root_agent",
]