"""Provider-neutral specialist definitions shared by all agent factories."""

from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel

from backend.agents.loader import load_prompt


@dataclass(frozen=True)
class Agent:
    name: str
    description: str
    instruction: str
    output_schema: type[BaseModel] | None = None
    sub_agents: list["Agent"] = field(default_factory=list)
    tools: list[Any] = field(default_factory=list)


def build_agent(
    *,
    name: str,
    prompt_folder: str,
    description: str,
    sub_agents: list[Agent] | None = None,
    tools: list[Any] | None = None,
    output_schema: type[BaseModel] | None = None,
) -> Agent:
    return Agent(
        name=name,
        description=description,
        instruction=load_prompt(prompt_folder, "system.md"),
        output_schema=output_schema,
        sub_agents=sub_agents or [],
        tools=tools or [],
    )
