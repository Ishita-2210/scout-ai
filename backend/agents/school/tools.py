"""
Tools used by the Scout School Agent.
"""

from typing import List

from backend.agents.school.schemas import SchoolResult


async def search_schools(
    location: str,
) -> List[SchoolResult]:
    """
    Search for schools near a location.

    This is currently a placeholder implementation.
    It will later integrate with:
        - Google Maps
        - Government Education APIs
        - UNESCO
        - UNHCR
    """

    return []