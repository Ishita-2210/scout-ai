"""
Scout Agent Bootstrap.

Registers all Scout agents during application startup.
"""

from backend.agents.registry import registry

from backend.agents.root import create_root_agent
from backend.agents.housing import (
    create_housing_agent,
)
from backend.agents.document import create_document_agent
from backend.agents.legal import (
    create_legal_agent,
)
from backend.agents.counselling import (
    create_counselling_agent,
)

from backend.agents.counselling.constants import (
    AGENT_NAME as COUNSELLING_AGENT_NAME,
)
from backend.agents.document.constants import (
    AGENT_NAME as DOCUMENT_AGENT_NAME,
)
from backend.agents.legal.constants import (
    AGENT_NAME as LEGAL_AGENT_NAME,
)
from backend.agents.housing.constants import (
    AGENT_NAME as HOUSING_AGENT_NAME,
)
from backend.agents.school import create_school_agent
from backend.agents.scholarship import (
    create_scholarship_agent,
)

from backend.agents.scholarship.constants import (
    AGENT_NAME as SCHOLARSHIP_AGENT_NAME,
)
from backend.agents.root.constants import (
    AGENT_NAME as ROOT_AGENT_NAME,
)

from backend.agents.school.constants import (
    AGENT_NAME as SCHOOL_AGENT_NAME,
)


def register_agents() -> None:
    """
    Register all Scout agents.

    Specialist agents are registered first so they
    can be injected into the Root Agent.
    """

    # Avoid duplicate registration
    if len(registry):
        return

    # ------------------------------------------------------
    # Register specialist agents
    # ------------------------------------------------------

    school_agent = create_school_agent()

    registry.register(
        SCHOOL_AGENT_NAME,
        school_agent,
    )

    scholarship_agent = create_scholarship_agent()

    registry.register(
        SCHOLARSHIP_AGENT_NAME,
        scholarship_agent,
    )

    document_agent = create_document_agent()

    registry.register(
        DOCUMENT_AGENT_NAME,
        document_agent,
    )

    housing_agent = create_housing_agent()

    registry.register(
        HOUSING_AGENT_NAME,
        housing_agent,
    )

    legal_agent = create_legal_agent()

    registry.register(
        LEGAL_AGENT_NAME,
        legal_agent,
    )

    counselling_agent = create_counselling_agent()

    registry.register(
        COUNSELLING_AGENT_NAME,
        counselling_agent,
    )
    # ------------------------------------------------------
    # Register Root Agent
    # ------------------------------------------------------

    root_agent = create_root_agent(
        sub_agents=registry.specialists(
            ROOT_AGENT_NAME,
        ),
    )

    registry.register(
        ROOT_AGENT_NAME,
        root_agent,
    )