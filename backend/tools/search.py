"""
Scout Search Tool.
"""

from backend.services.search_service import search_service


async def search_web(
    query: str,
) -> dict:
    """
    Search the web.
    """

    response = await search_service.search(
        query=query,
    )

    return response.model_dump()


__all__ = (
    "search_web",
)