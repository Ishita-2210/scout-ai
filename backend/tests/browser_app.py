"""Browser-test server: real app/storage/routes with Groq mocked at HTTP transport.
Never import this module for deployment. No production demo/fallback is installed.
"""

import asyncio
import json
import os
import tempfile
from pathlib import Path

os.environ["DATABASE_URL"] = (
    "sqlite:///" + (Path(tempfile.mkdtemp(prefix="scout-browser-")) / "test.db").as_posix()
)
os.environ["GROQ_API_KEY"] = "browser-test-key"
os.environ["SESSION_SECRET"] = "browser-test-secret-" * 4
os.environ["SERPER_API_KEY"] = ""
os.environ["SECURE_COOKIES"] = "false"

import groq
import httpx

from backend import config
from backend.main import app as app
from backend.services.ai_service import ai_service


async def mock_groq(request):
    assert str(request.url) == "https://api.groq.com/openai/v1/chat/completions"
    payload = json.loads(request.content)
    name = payload["response_format"]["json_schema"]["name"]
    message = payload["messages"][-1]["content"]
    if "CANCEL_TEST" in message:
        await asyncio.sleep(60)
    if "RATE_LIMIT_TEST" in message:
        return httpx.Response(429, headers={"retry-after": "10"}, json={"error": {"message": "rate limit"}})
    if name == "RoutePlan":
        answer = {
            "tasks": [{"domain": "document", "search_query": None}],
            "reply": None,
            "profile": {"grade": "8"},
        }
    else:
        answer = {
            "guidance": "You can take this one step at a time.\n\n1. Contact your previous school for a duplicate transfer certificate.\n2. Ask your new school which temporary records they can accept.\n\nTell me your **state and education board** so we can work out the next step. Current procedures need official confirmation.",
            "data": {
                "query": message,
                "documents": [
                    {
                        "name": "Transfer certificate",
                        "required": True,
                        "available": False,
                        "issuing_authority": "Previous school",
                        "replacement_process": "Ask the school office about duplicate records.",
                    }
                ],
                "summary": "Start with your previous school.",
            },
        }
    return httpx.Response(
        200,
        json={
            "id": "browser-test",
            "object": "chat.completion",
            "created": 1,
            "model": payload["model"],
            "choices": [
                {
                    "index": 0,
                    "finish_reason": "stop",
                    "message": {"role": "assistant", "content": json.dumps(answer)},
                }
            ],
        },
    )


ai_service.client = groq.AsyncGroq(
    base_url=config.GROQ_BASE_URL,
    api_key="browser-test-key",
    max_retries=0,
    http_client=httpx.AsyncClient(transport=httpx.MockTransport(mock_groq)),
)
