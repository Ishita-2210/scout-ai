"""
Scout Search Service.

Provides web search functionality for Scout using
the Serper Search API.
"""

from typing import Final
import logging

import httpx

from backend.config import (
    SEARCH_TIMEOUT,
    SERPER_API_KEY,
    SERPER_URL,
)
from backend.models import (
    SearchResponse,
    SearchResult,
)

logger = logging.getLogger(__name__)

MAX_RESULTS: Final = 5


class SearchService:
    """
    Service responsible for performing web searches.
    """

    async def search(
        self,
        query: str,
    ) -> SearchResponse:
        """
        Perform a web search.

        Parameters
        ----------
        query:
            Search query.

        Returns
        -------
        SearchResponse
            Normalized search results.
        """

        logger.info(
            "Searching for '%s'.",
            query,
        )

        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json",
        }

        payload = {
            "q": query,
        }

        try:

            async with httpx.AsyncClient(
                timeout=SEARCH_TIMEOUT,
            ) as client:

                response = await client.post(
                    SERPER_URL,
                    headers=headers,
                    json=payload,
                )

                response.raise_for_status()

        except httpx.TimeoutException as exc:

            logger.exception(
                "Search request timed out."
            )

            raise RuntimeError(
                "Search request timed out."
            ) from exc

        except httpx.HTTPStatusError as exc:

            logger.exception(
                "Search request failed."
            )

            raise RuntimeError(
                f"Search failed ({exc.response.status_code})."
            ) from exc

        except Exception as exc:

            logger.exception(
                "Unexpected search error."
            )

            raise RuntimeError(
                "Unexpected search failure."
            ) from exc

        data = response.json()

        results = [
            SearchResult(
                title=result.get("title", ""),
                url=result.get("link", ""),
                snippet=result.get("snippet", ""),
            )
            for result in data.get("organic", [])[:MAX_RESULTS]
        ]
        
        logger.info(
            "Retrieved %d search results.",
            len(results),
        )

        return SearchResponse(
            query=query,
            results=results,
        )


search_service = SearchService()


__all__ = (
    "SearchService",
    "search_service",
)