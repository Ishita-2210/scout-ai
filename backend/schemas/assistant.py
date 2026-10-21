"""Validated internal routing and public result contracts."""

from typing import Literal

from pydantic import Field

from backend.memory.models import MemoryUpdate
from backend.models.common import DomainModel

Domain = Literal["school", "scholarship", "document", "housing", "legal", "counselling"]


class Task(DomainModel):
    domain: Domain
    search_query: str | None = Field(default=None, max_length=300)


class RoutePlan(DomainModel):
    tasks: list[Task] = Field(max_length=6)
    reply: str | None = Field(default=None, max_length=6000)
    profile: MemoryUpdate


class Source(DomainModel):
    title: str
    url: str


class Section(DomainModel):
    domain: Domain
    title: str
    guidance: str
    data: dict


class AssistantResult(DomainModel):
    text: str
    sections: list[Section] = Field(default_factory=list)
    sources: list[Source] = Field(default_factory=list)
    references: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
