"""
Schemas used by the Scout School Agent.
"""

from pydantic import BaseModel, Field


class SchoolSearchRequest(BaseModel):
    """
    Request sent to the School Agent.
    """

    location: str = Field(
        ...,
        description="Student's current location.",
    )


class SchoolResult(BaseModel):
    """
    Represents a recommended school.
    """

    name: str = Field(
        ...,
        description="School name.",
    )

    address: str = Field(
        ...,
        description="School address.",
    )

    website: str | None = Field(
        default=None,
        description="Official school website.",
    )


class SchoolSearchResponse(BaseModel):
    """
    Response returned by the School Agent.
    """

    schools: list[SchoolResult]