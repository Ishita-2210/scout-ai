"""
Scout Document Agent.

Defines the specialist agent responsible for helping
students with admission documents.
"""

from google.adk.agents import Agent

from backend.agents.agent_builder import build_agent
from backend.agents.document.constants import (
    AGENT_NAME,
    DESCRIPTION,
    PROMPT_FOLDER,
)
from backend.models import (
    DocumentChecklist,
)
from backend.tools import search_web


def create_document_agent() -> Agent:
    """
    Create the Scout Document Agent.
    """

    return build_agent(
        name=AGENT_NAME,
        prompt_folder=PROMPT_FOLDER,
        description=DESCRIPTION,
        tools=[
            search_web,
        ],
        output_schema=DocumentChecklist,
    )


__all__ = (
    "create_document_agent",
)