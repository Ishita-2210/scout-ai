"""
Scout Agent Registration.

Registers every Scout agent with the
central registry.
"""

from __future__ import annotations

import logging

from backend.agents.registry import (
    registry,
)

from backend.agents.root.agent import (
    create_root_agent,
)

from backend.agents.root.constants import (
    AGENT_NAME as ROOT_AGENT_NAME,
)

from backend.agents.school.agent import (
    create_school_agent,
)

from backend.agents.scholarship.agent import (
    create_scholarship_agent,
)

from backend.agents.document.agent import (
    create_document_agent,
)

from backend.agents.housing.agent import (
    create_housing_agent,
)

from backend.agents.legal.agent import (
    create_legal_agent,
)

from backend.agents.counselling.agent import (
    create_counselling_agent,
)

logger = logging.getLogger(__name__)

# ==========================================================
# Registration
# ==========================================================


def register_agents() -> None:
    """
    Create and register every Scout agent.

    Safe to call multiple times.
    """

    if ROOT_AGENT_NAME in registry:

        logger.info(
            "Agents already registered.",
        )

        return

    logger.info(
        "Registering Scout agents...",
    )

    # ------------------------------------------------------
    # Specialist Agents
    # ------------------------------------------------------

    school_agent = create_school_agent()

    scholarship_agent = create_scholarship_agent()

    document_agent = create_document_agent()

    housing_agent = create_housing_agent()

    legal_agent = create_legal_agent()

    counselling_agent = create_counselling_agent()

    specialists = [
        school_agent,
        scholarship_agent,
        document_agent,
        housing_agent,
        legal_agent,
        counselling_agent,
    ]

    # ------------------------------------------------------
    # Register Specialists
    # ------------------------------------------------------
    print("\n=== Agents to register ===")
    for agent in specialists:
        print(agent.name)
        print("==========================\n")
    for agent in specialists:

        registry.register(
            agent.name,
            agent,
        )

    # ------------------------------------------------------
    # Root Agent
    # ------------------------------------------------------

    root_agent = create_root_agent(
        sub_agents=specialists,
    )

    registry.register(
        ROOT_AGENT_NAME,
        root_agent,
    )

    logger.info(
        "Successfully registered %d agents.",
        len(registry),
    )


__all__ = (
    "register_agents",
)