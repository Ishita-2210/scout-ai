"""
Scout Scholarship Agent Metadata.
"""

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True, slots=True)
class AgentMetadata:
    """
    Metadata describing a Scout agent.
    """

    name: str
    description: str
    responsibilities: tuple[str, ...]


METADATA: Final = AgentMetadata(
    name="scholarship_agent",
    description=(
        "Helps students discover scholarships, "
        "financial aid, grants, and educational funding."
    ),
    responsibilities=(
        "scholarships",
        "financial aid",
        "government schemes",
        "education grants",
        "fee waivers",
        "student funding",
    ),
)


__all__ = (
    "AgentMetadata",
    "METADATA",
)