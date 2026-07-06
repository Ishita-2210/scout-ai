"""
Scout Housing Agent Metadata.
"""

from typing import Final

from backend.agents.metadata import AgentMetadata


METADATA: Final = AgentMetadata(
    name="housing_agent",
    description=(
        "Helps displaced students and families find "
        "temporary accommodation and housing."
    ),
    responsibilities=(
        "temporary housing",
        "student hostels",
        "government shelters",
        "relief camps",
        "ngo accommodation",
        "safe housing",
        "residential schools",
        "accommodation near schools",
    ),
)


__all__ = (
    "METADATA",
)