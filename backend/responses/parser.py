"""
Scout Response Parser.

Converts raw ADK outputs into normalized
Scout response objects.
"""

from typing import Any

from pydantic import BaseModel

from backend.responses.models import AgentResponse
from backend.responses.types import ResponseType


class ResponseParser:
    """
    Parses agent outputs into normalized responses.
    """

    def parse(
        self,
        response: Any,
        *,
        source_agent: str | None = None,
    ) -> AgentResponse:
        """
        Normalize an agent response.
        """

        if isinstance(response, BaseModel):

            return AgentResponse(
                response_type=ResponseType.STRUCTURED,
                content=response.model_dump(),
                source_agent=source_agent,
            )

        if isinstance(response, dict):

            return AgentResponse(
                response_type=ResponseType.STRUCTURED,
                content=response,
                source_agent=source_agent,
            )

        return AgentResponse(
            response_type=ResponseType.TEXT,
            content=str(response),
            source_agent=source_agent,
        )


response_parser = ResponseParser()


__all__ = (
    "ResponseParser",
    "response_parser",
)