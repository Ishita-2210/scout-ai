"""
Scout Root Agent Metadata.
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
    name="root_agent",
    description=(
        "Coordinates specialist agents and manages "
        "conversation orchestration."
    ),
    responsibilities=(
        "orchestration",
        "routing",
        "delegation",
        "conversation",
    ),
)


__all__ = (
    "AgentMetadata",
    "METADATA",
)