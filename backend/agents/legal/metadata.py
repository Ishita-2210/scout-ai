"""
Scout Legal Agent Metadata.
"""

from typing import Final

from backend.agents.metadata import AgentMetadata


METADATA: Final = AgentMetadata(
    name="legal_agent",
    description=(
        "Helps displaced students understand educational "
        "rights, policies, and government procedures."
    ),
    responsibilities=(
        "right to education",
        "child rights",
        "education laws",
        "government policies",
        "school admission rights",
        "education notifications",
        "legal aid",
        "government schemes",
        "education regulations",
        "official procedures",
    ),
)


__all__ = (
    "METADATA",
)