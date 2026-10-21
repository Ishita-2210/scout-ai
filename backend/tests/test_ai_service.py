import asyncio
import json
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime

import groq
import httpx
import pytest
from pydantic import BaseModel, ConfigDict

from backend import config
from backend.services.ai_service import AIError, AIService, duration, strict_schema


class Answer(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str


def completion(content='{"text":"A real mock response"}', finish="stop"):
    return {
        "id": "chat-test",
        "object": "chat.completion",
        "created": 1,
        "model": config.GROQ_MODEL,
        "choices": [
            {"index": 0, "finish_reason": finish, "message": {"role": "assistant", "content": content}}
        ],
    }


async def exercise(handler, action=None):
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    client = groq.AsyncGroq(api_key="test", base_url=config.GROQ_BASE_URL, http_client=http, max_retries=0)
    service = AIService(client)
    try:
        if action:
            return await action(service)
        return await service.complete([{"role": "user", "content": "Hello"}], Answer, "test-id")
    finally:
        await service.close()


def test_sdk_payload_and_validated_result():
    def handler(request):
        body = json.loads(request.content)
        assert body["model"] == config.GROQ_MODEL
        assert body["response_format"]["json_schema"]["strict"] is True
        assert body["max_completion_tokens"] == config.AI_MAX_TOKENS
        assert request.url.path == "/openai/v1/chat/completions"
        return httpx.Response(200, json=completion())

    assert asyncio.run(exercise(handler)).text == "A real mock response"


def test_production_client_initialization_uses_exact_groq_endpoint(monkeypatch):
    real_client = groq.AsyncGroq
    urls = []

    def handler(request):
        urls.append(str(request.url))
        return httpx.Response(200, json=completion())

    def create_client(**kwargs):
        return real_client(**kwargs, http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)))

    monkeypatch.setattr("backend.services.ai_service.groq.AsyncGroq", create_client)

    async def run():
        service = AIService()
        try:
            result = await service.complete([{"role": "user", "content": "Hello"}], Answer, "test-init")
            assert result.text == "A real mock response"
        finally:
            await service.close()

    asyncio.run(run())
    assert urls == ["https://api.groq.com/openai/v1/chat/completions"]


@pytest.mark.parametrize(
    "status,code",
    [
        (401, "authentication"),
        (403, "authentication"),
        (400, "model_configuration"),
        (404, "model_configuration"),
    ],
)
def test_non_retryable_provider_errors(status, code):
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(status, json={"error": {"message": "secret provider detail"}})

    with pytest.raises(AIError) as exc:
        asyncio.run(exercise(handler))
    assert exc.value.code == code
    assert "secret" not in exc.value.message
    assert len(calls) == 1


def test_transient_failure_has_bounded_retries(monkeypatch):
    calls, sleeps = [], []

    async def sleep(delay):
        sleeps.append(delay)

    monkeypatch.setattr("backend.services.ai_service.asyncio.sleep", sleep)

    def handler(request):
        calls.append(request)
        return httpx.Response(503, json={"error": {"message": "outage"}})

    with pytest.raises(AIError):
        asyncio.run(exercise(handler))
    assert len(calls) == 3
    assert len(sleeps) == 2
    assert 0.5 <= sleeps[0] <= 0.75 and 1 <= sleeps[1] <= 1.25


def test_retry_after_is_respected(monkeypatch):
    calls, sleeps = [], []

    async def sleep(delay):
        sleeps.append(delay)

    monkeypatch.setattr("backend.services.ai_service.asyncio.sleep", sleep)

    def handler(request):
        calls.append(request)
        return (
            httpx.Response(429, headers={"retry-after": "2"}, json={"error": {"message": "rate limit"}})
            if len(calls) == 1
            else httpx.Response(200, json=completion())
        )

    asyncio.run(exercise(handler))
    assert len(calls) == 2 and 2 <= sleeps[0] <= 2.25


@pytest.mark.parametrize(
    "headers,body",
    [
        ({"retry-after": "3600", "x-ratelimit-remaining-requests": "0"}, "limit"),
        ({"retry-after": "300"}, "tokens per day exceeded"),
    ],
)
def test_daily_quota_is_not_retried_and_blocks_followups(headers, body):
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(429, headers=headers, json={"error": {"message": body}})

    async def action(service):
        for _ in range(2):
            with pytest.raises(AIError) as exc:
                await service.complete([], Answer, "id")
            assert exc.value.code == "quota_exhausted"
            assert exc.value.retry_after >= 299

    asyncio.run(exercise(handler, action))
    assert len(calls) == 1


def test_long_rate_reset_is_returned_without_sleep():
    def handler(request):
        return httpx.Response(429, headers={"retry-after": "35"}, json={"error": {"message": "limit"}})

    with pytest.raises(AIError) as exc:
        asyncio.run(exercise(handler))
    assert exc.value.status == 429 and exc.value.retry_after == 35


@pytest.mark.parametrize(
    "content,finish",
    [
        ("invalid JSON", "stop"),
        ('{"text":3}', "stop"),
        ('{"text":"ok","unexpected":true}', "stop"),
        ('{"text":"truncated', "length"),
        (None, "stop"),
    ],
)
def test_bad_output_never_becomes_a_fake_answer(content, finish):
    with pytest.raises(AIError) as exc:
        asyncio.run(exercise(lambda request: httpx.Response(200, json=completion(content, finish))))
    assert exc.value.status == 502


def test_timeout_is_not_replayed():
    calls = []

    def handler(request):
        calls.append(request)
        raise httpx.ReadTimeout("timeout", request=request)

    with pytest.raises(AIError) as exc:
        asyncio.run(exercise(handler))
    assert exc.value.code == "timeout" and len(calls) == 1


def test_missing_key(monkeypatch):
    monkeypatch.setattr(config, "GROQ_API_KEY", "")
    with pytest.raises(AIError) as exc:
        asyncio.run(AIService().complete([], Answer, "id"))
    assert exc.value.code == "configuration"


def test_invalid_provider_envelope():
    with pytest.raises(AIError) as exc:
        asyncio.run(exercise(lambda request: httpx.Response(200, json={"choices": [None]})))
    assert exc.value.code == "invalid_response"


def test_provider_concurrency_is_bounded():
    async def run():
        active, peak = 0, 0

        async def handler(request):
            nonlocal active, peak
            active += 1
            peak = max(peak, active)
            await asyncio.sleep(0.02)
            active -= 1
            return httpx.Response(200, json=completion())

        async def action(service):
            await asyncio.gather(*[service.complete([], Answer, str(i)) for i in range(5)])

        await exercise(handler, action)
        assert peak == config.AI_CONCURRENCY

    asyncio.run(run())


def test_header_durations_and_schema():
    assert duration("2m3.5s") == 123.5
    assert duration("500ms") == 0.5
    assert 58 <= duration(format_datetime(datetime.now(timezone.utc) + timedelta(seconds=60))) <= 60
    from backend.schemas.assistant import RoutePlan

    schema = strict_schema(RoutePlan.model_json_schema())
    for definition in [schema, *schema["$defs"].values()]:
        if definition.get("type") == "object":
            assert definition["additionalProperties"] is False
            assert set(definition["required"]) == set(definition["properties"])
