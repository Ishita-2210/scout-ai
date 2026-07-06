"""
Scout Document Agent Metadata.
"""

from typing import Final

from backend.agents.metadata import AgentMetadata


METADATA: Final = AgentMetadata(
    name="document_agent",
    description=(
        "Helps students understand admission documents "
        "and recover missing educational records."
    ),
    responsibilities=(
        "admission documents",
        "birth certificate",
        "transfer certificate",
        "marksheet",
        "identity proof",
        "income certificate",
        "caste certificate",
        "document recovery",
    ),
)


__all__ = (
    "METADATA",
)