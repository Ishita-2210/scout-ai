"""
Scout Agent Registry.

Central registry for all Scout agents.
"""

from __future__ import annotations

from google.adk.agents import Agent


# ==========================================================
# Agent Registry
# ==========================================================


class AgentRegistry:
    """
    Registry responsible for storing,
    retrieving, and managing Scout agents.
    """

    def __init__(self) -> None:

        self._agents: dict[str, Agent] = {}

    # ======================================================
    # Registration
    # ======================================================

    def register(
        self,
        name: str,
        agent: Agent,
    ) -> None:
        """
        Register a new agent.
        """

        if name in self._agents:

            raise ValueError(
                f"Agent '{name}' is already registered."
            )

        self._agents[name] = agent

    def remove(
        self,
        name: str,
    ) -> None:
        """
        Remove a registered agent.
        """

        if name not in self._agents:

            raise KeyError(
                f"Agent '{name}' is not registered."
            )

        del self._agents[name]

    def clear(
        self,
    ) -> None:
        """
        Remove every registered agent.

        Intended primarily for testing.
        """

        self._agents.clear()

    # ======================================================
    # Lookup
    # ======================================================

    def get(
        self,
        name: str,
    ) -> Agent:
        """
        Retrieve an agent by name.
        """

        try:

            return self._agents[name]

        except KeyError as exc:

            raise KeyError(
                f"Agent '{name}' is not registered."
            ) from exc

    def has(
        self,
        name: str,
    ) -> bool:
        """
        Determine whether an agent exists.
        """

        return name in self._agents

    # ======================================================
    # Collections
    # ======================================================

    def names(
        self,
    ) -> list[str]:
        """
        Return all registered agent names.
        """

        return sorted(
            self._agents.keys(),
        )

    def list_agents(
        self,
    ) -> list[str]:
        """
        Backwards-compatible alias.
        """

        return self.names()

    def values(
        self,
    ) -> list[Agent]:
        """
        Return every registered agent.
        """

        return list(
            self._agents.values(),
        )

    def items(
        self,
    ) -> list[tuple[str, Agent]]:
        """
        Return registry items.
        """

        return list(
            self._agents.items(),
        )

    def specialists(
        self,
        root_agent_name: str,
    ) -> list[Agent]:
        """
        Return every specialist agent.

        The Root Agent is excluded.
        """

        return [
            agent
            for name, agent
            in self._agents.items()
            if name != root_agent_name
        ]

    # ======================================================
    # Dunder Methods
    # ======================================================

    def __contains__(
        self,
        name: str,
    ) -> bool:

        return name in self._agents

    def __len__(
        self,
    ) -> int:

        return len(
            self._agents,
        )


registry = AgentRegistry()


__all__ = (
    "AgentRegistry",
    "registry",
)