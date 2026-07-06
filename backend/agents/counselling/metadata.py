"""
Scout Counselling Agent Metadata.
"""

from typing import Final

from backend.agents.metadata import AgentMetadata


METADATA: Final = AgentMetadata(
    name="counselling_agent",
    description=(
        "Provides educational encouragement, emotional support, "
        "study planning, and wellbeing guidance for displaced students."
    ),
    responsibilities=(
        "student wellbeing",
        "emotional support",
        "stress management",
        "study planning",
        "motivation",
        "confidence building",
        "goal setting",
        "school re-engagement",
        "educational resilience",
        "learning habits",
    ),
)


__all__ = (
    "METADATA",
)