"""Scout API and same-origin production frontend."""

import logging
import time
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from backend import config
from backend.agents.register import register_agents
from backend.api.chat import router
from backend.database import create_tables
from backend.services.ai_service import ai_service

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
# Provider HTTP logs can include URLs or response metadata. Our boundary logs safe categories.
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app):
    if config.SECURE_COOKIES and len(config.SESSION_SECRET) < 32:
        raise RuntimeError("Set a stable SESSION_SECRET of at least 32 characters for production.")
    if not config.SESSION_SECRET:
        logger.warning("SESSION_SECRET is unset; development browser sessions expire on server restart.")
    create_tables()
    register_agents()
    yield
    await ai_service.close()


app = FastAPI(
    title="Scout API",
    description="Education continuity support for displaced students.",
    version="2.0.0",
    lifespan=lifespan,
)


class BodyLimitMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope["method"] not in {"POST", "PUT", "PATCH"}:
            return await self.app(scope, receive, send)
        body = bytearray()
        while True:
            event = await receive()
            if event["type"] == "http.disconnect":
                return
            body.extend(event.get("body", b""))
            if len(body) > config.MAX_BODY_BYTES:
                return await JSONResponse({"detail": "Request is too large."}, status_code=413)(
                    scope, receive, send
                )
            if not event.get("more_body", False):
                break
        delivered = False

        async def replay():
            nonlocal delivered
            if not delivered:
                delivered = True
                return {"type": "http.request", "body": bytes(body), "more_body": False}
            return await receive()

        await self.app(scope, replay, send)


app.add_middleware(BodyLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type"],
    expose_headers=["Retry-After", "X-Request-ID"],
)


@app.middleware("http")
async def request_context(request: Request, call_next):
    request.state.request_id = str(uuid4())
    started = time.monotonic()
    try:
        response = await call_next(request)
    except Exception as exc:
        logger.error(
            "request_id=%s category=internal exception_type=%s", request.state.request_id, type(exc).__name__
        )
        response = JSONResponse(
            {"detail": "Scout encountered a server error. Please try later."}, status_code=500
        )
    response.headers["X-Request-ID"] = request.state.request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'"
    )
    if request.url.path in {"/docs", "/redoc"}:
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
            "style-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
            "img-src 'self' data: https://fastapi.tiangolo.com; object-src 'none'; frame-ancestors 'none'"
        )
    if request.url.path.startswith("/api"):
        response.headers["Cache-Control"] = "no-store"
    logger.info(
        "request_id=%s method=%s status=%d latency_ms=%d",
        request.state.request_id,
        request.method,
        response.status_code,
        (time.monotonic() - started) * 1000,
    )
    return response


@app.exception_handler(RequestValidationError)
async def invalid_input(request, exc):
    return JSONResponse(
        {
            "detail": "Check your message and conversation identifiers. Messages must contain 1 to 4,000 characters."
        },
        status_code=422,
    )


app.include_router(router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "Scout", "version": "2.0.0"}


DIST = config.ROOT / "frontend" / "dist"
if (DIST / "assets").exists():
    app.mount("/assets", StaticFiles(directory=DIST / "assets"), name="assets")


@app.get("/favicon.svg")
async def favicon():
    return FileResponse(config.ROOT / "frontend" / "public" / "favicon.svg")


@app.get("/")
async def root():
    if (DIST / "index.html").exists():
        return FileResponse(DIST / "index.html")
    return {"message": "Scout API is running. Start the Vite frontend or build frontend/dist."}
