from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AgentMetadata:
    """
    Metadata describing a Scout agent.
    """

    name: str
    description: str
    responsibilities: tuple[str, ...]


__all__ = (
    "AgentMetadata",
)