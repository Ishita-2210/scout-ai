"""The only LLM boundary: bounded concurrency, validated JSON and safe failures."""

import asyncio
import logging
import random
import re
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import TypeVar

import groq
from pydantic import BaseModel, ValidationError

from backend import config

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)


class AIError(Exception):
    def __init__(self, code: str, message: str, status: int = 503, retry_after: int | None = None):
        super().__init__(message)
        self.code, self.message, self.status, self.retry_after = code, message, status, retry_after


def duration(value: str | None) -> float:
    if not value:
        return 0
    try:
        return max(0, float(value))
    except ValueError:
        try:
            return max(0, (parsedate_to_datetime(value) - datetime.now(timezone.utc)).total_seconds())
        except (ValueError, TypeError, OverflowError):
            units = {"h": 3600, "m": 60, "s": 1, "ms": 0.001}
            return sum(float(n) * units[u] for n, u in re.findall(r"([\d.]+)(ms|h|m|s)", value))


def strict_schema(schema: dict) -> dict:
    """Strict mode requires every object property, including nullable defaults."""
    schema = {k: v for k, v in schema.items() if k != "default"}
    if schema.get("type") == "object":
        schema["additionalProperties"] = False
        schema["required"] = list(schema.get("properties", {}))
    return {
        k: strict_schema(v)
        if isinstance(v, dict)
        else [strict_schema(i) if isinstance(i, dict) else i for i in v]
        if isinstance(v, list)
        else v
        for k, v in schema.items()
    }


class AIService:
    def __init__(self, client=None):
        self.client = client
        self.slots = asyncio.Semaphore(config.AI_CONCURRENCY)
        self.blocked_until = 0.0
        self.blocked_error: AIError | None = None

    async def close(self):
        if self.client:
            await self.client.close()
            self.client = None

    async def complete(self, messages: list[dict], schema: type[T], request_id: str) -> T:
        if not self.client:
            if not config.GROQ_API_KEY:
                raise AIError(
                    "configuration", "Scout is not configured yet. Ask the administrator to set GROQ_API_KEY."
                )
            self.client = groq.AsyncGroq(
                api_key=config.GROQ_API_KEY,
                base_url=config.GROQ_BASE_URL,
                timeout=config.AI_TIMEOUT,
                max_retries=0,
            )
        async with self.slots:
            for attempt in range(3):
                if time.monotonic() < self.blocked_until and self.blocked_error:
                    raise AIError(
                        self.blocked_error.code,
                        self.blocked_error.message,
                        429,
                        max(1, int(self.blocked_until - time.monotonic())),
                    )
                started = time.monotonic()
                try:
                    raw = await self.client.chat.completions.with_raw_response.create(
                        model=config.GROQ_MODEL,
                        messages=messages,
                        max_completion_tokens=config.AI_MAX_TOKENS,
                        response_format={
                            "type": "json_schema",
                            "json_schema": {
                                "name": schema.__name__,
                                "strict": True,
                                "schema": strict_schema(schema.model_json_schema()),
                            },
                        },
                    )
                    response = await raw.parse()
                    logger.info(
                        "ai request_id=%s status=200 latency_ms=%d attempt=%d",
                        request_id,
                        (time.monotonic() - started) * 1000,
                        attempt + 1,
                    )
                    if not response.choices or response.choices[0].finish_reason != "stop":
                        raise AIError(
                            "incomplete_response",
                            "Scout could not finish that answer. Try a shorter, more specific question.",
                            502,
                        )
                    try:
                        result = schema.model_validate_json(
                            response.choices[0].message.content or "", strict=True
                        )
                    except (ValidationError, ValueError) as exc:
                        raise AIError(
                            "invalid_response", "Scout returned an unreadable answer. Please try again.", 502
                        ) from exc
                    self._observe_limits(raw.headers)
                    return result
                except groq.APIStatusError as exc:
                    status, headers = exc.status_code, exc.response.headers
                    logger.warning(
                        "ai request_id=%s status=%d latency_ms=%d attempt=%d",
                        request_id,
                        status,
                        (time.monotonic() - started) * 1000,
                        attempt + 1,
                    )
                    if status in (401, 403):
                        raise AIError(
                            "authentication",
                            "The AI service credentials need attention. Contact the administrator.",
                        ) from exc
                    if status in (400, 404, 422):
                        raise AIError(
                            "model_configuration",
                            "The AI model configuration needs attention. Contact the administrator.",
                        ) from exc
                    if status == 429:
                        body = str(exc.body).lower()
                        daily = headers.get("x-ratelimit-remaining-requests") == "0" or any(
                            term in body
                            for term in (
                                "tokens per day",
                                "requests per day",
                                "daily",
                                "quota_exceeded",
                                "quota exhausted",
                            )
                        )
                        delay = max(
                            duration(headers.get("retry-after")),
                            duration(headers.get("x-ratelimit-reset-requests"))
                            if daily
                            else duration(headers.get("x-ratelimit-reset-tokens")),
                        )
                        error = AIError(
                            "quota_exhausted" if daily else "rate_limit",
                            "The AI daily quota is exhausted. Try after the quota resets."
                            if daily
                            else "Scout is receiving too many requests. Please wait before trying again.",
                            429,
                            max(3600 if daily and not delay else 1, int(delay + 0.999)),
                        )
                        if daily or delay > 8 or attempt == 2:
                            self.blocked_until = time.monotonic() + error.retry_after
                            self.blocked_error = error
                            raise error from exc
                    elif status not in (500, 502, 503, 504):
                        raise AIError(
                            "provider_failure", "The AI service could not process this request.", 502
                        ) from exc
                    else:
                        delay = duration(headers.get("retry-after"))
                    if attempt == 2 or delay > 8:
                        raise AIError(
                            "provider_unavailable",
                            "The AI service is temporarily unavailable. Please try later.",
                            503,
                            max(1, int(delay)) if delay else None,
                        ) from exc
                    await asyncio.sleep(max(delay, 0.5 * 2**attempt) + random.uniform(0, 0.25))
                except groq.APITimeoutError as exc:
                    # A timed-out request may already have been generated/billed: do not replay it.
                    raise AIError(
                        "timeout", "Scout took too long to respond. Please try again.", 504
                    ) from exc
                except groq.APIConnectionError as exc:
                    raise AIError(
                        "connection", "The AI service could not be reached. Please try later."
                    ) from exc
                except (
                    groq.APIResponseValidationError,
                    AttributeError,
                    KeyError,
                    IndexError,
                    TypeError,
                ) as exc:
                    raise AIError(
                        "invalid_response", "Scout returned an unreadable answer. Please try again.", 502
                    ) from exc
        raise AIError("provider_unavailable", "The AI service is temporarily unavailable.")

    def _observe_limits(self, headers):
        daily = headers.get("x-ratelimit-remaining-requests") == "0"
        tokens = headers.get("x-ratelimit-remaining-tokens") == "0"
        if daily or tokens:
            delay = duration(
                headers.get("x-ratelimit-reset-requests" if daily else "x-ratelimit-reset-tokens")
            )
            self.blocked_until = time.monotonic() + max(3600 if daily and not delay else 1, delay)
            self.blocked_error = AIError(
                "quota_exhausted" if daily else "rate_limit",
                "The AI daily quota is exhausted. Try after the quota resets."
                if daily
                else "Scout needs a moment before the next request. Please try shortly.",
                429,
            )


ai_service = AIService()
