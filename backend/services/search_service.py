"""Server-side Serper search. Queries and credentials never appear in logs."""

import httpx

from backend import config
from backend.models.search import SearchResponse, SearchResult


class SearchService:
    async def search(self, query: str) -> SearchResponse:
        if not config.SERPER_API_KEY:
            raise RuntimeError("Live search is not configured.")
        try:
            async with httpx.AsyncClient(timeout=config.SEARCH_TIMEOUT) as client:
                response = await client.post(
                    config.SERPER_URL,
                    headers={"X-API-KEY": config.SERPER_API_KEY},
                    json={"q": query[:300], "num": 5},
                )
                response.raise_for_status()
                data = response.json()
                results = [
                    SearchResult(
                        title=str(r.get("title", ""))[:300],
                        url=str(r.get("link", ""))[:2000],
                        snippet=str(r.get("snippet", ""))[:1000],
                    )
                    for r in data.get("organic", [])[:5]
                    if isinstance(r, dict)
                ]
                return SearchResponse(query=query, results=results)
        except (httpx.HTTPError, ValueError, TypeError, AttributeError) as exc:
            raise RuntimeError("Live search is unavailable.") from exc


search_service = SearchService()
