"""Signed anonymous browser identity. Client-supplied user IDs are never trusted."""

import hashlib
import hmac
import secrets
import time
from collections import OrderedDict, deque
from uuid import uuid4

from fastapi import HTTPException, Request, Response

from backend import config

COOKIE = "scout_session"
TTL = 60 * 60 * 24 * 30
SECRET = config.SESSION_SECRET or secrets.token_hex(32)


def check_origin(request: Request):
    origin = request.headers.get("origin")
    if origin and origin not in config.ALLOWED_ORIGINS and origin != str(request.base_url).rstrip("/"):
        raise HTTPException(403, "This origin is not allowed.")


def identity(request: Request) -> str:
    value = request.cookies.get(COOKIE, "")
    try:
        owner, expires, signature = value.split(".")
        expected = hmac.new(SECRET.encode(), f"{owner}.{expires}".encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected) or int(expires) < time.time() or len(owner) != 36:
            raise ValueError
        return owner
    except (ValueError, TypeError):
        raise HTTPException(401, "Your session has expired. Refresh to start a new session.") from None


def issue_identity(request: Request, response: Response):
    try:
        return identity(request)
    except HTTPException:
        owner, expires = str(uuid4()), str(int(time.time()) + TTL)
        payload = f"{owner}.{expires}"
        signature = hmac.new(SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
        response.set_cookie(
            COOKIE,
            f"{payload}.{signature}",
            max_age=TTL,
            httponly=True,
            secure=config.SECURE_COOKIES,
            samesite="lax",
            path="/",
        )
        return owner


class RateLimiter:
    """Bounded in-process sliding window; deploy behind a shared ingress limiter."""

    def __init__(self):
        self.buckets = OrderedDict()

    def check(self, key: str, limit: int):
        now = time.monotonic()
        bucket = self.buckets.setdefault(key, deque())
        self.buckets.move_to_end(key)
        while bucket and bucket[0] <= now - 60:
            bucket.popleft()
        if len(bucket) >= limit:
            raise HTTPException(
                429,
                "Too many requests. Please wait before trying again.",
                headers={"Retry-After": str(max(1, int(61 - now + bucket[0])))},
            )
        bucket.append(now)
        while len(self.buckets) > 10000:
            self.buckets.popitem(last=False)


limiter = RateLimiter()
