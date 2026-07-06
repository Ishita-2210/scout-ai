"""
Scout Search Models.
"""

from pydantic import Field

from backend.models.common import DomainModel


class SearchResult(DomainModel):
    """
    Represents a single web search result.
    """

    title: str = Field(
        description="Result title.",
    )

    url: str = Field(
        description="Source URL.",
    )

    snippet: str = Field(
        description="Short description.",
    )


class SearchResponse(DomainModel):
    """
    Search response.
    """

    query: str = Field(
        description="Original query.",
    )

    results: list[SearchResult] = Field(
        default_factory=list,
        description="Search results.",
    )


__all__ = (
    "SearchResult",
    "SearchResponse",
)