"""
Scout Backend.

Application entry point.
"""

from __future__ import annotations
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.database import create_tables

from backend.agents.register import register_agents

from backend.api.chat import router as chat_router

logger = logging.getLogger(__name__)


# ==========================================================
# Application Lifespan
# ==========================================================


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    """
    Application startup and shutdown.
    """

    logger.info(
        "Starting Scout backend...",
    )

    create_tables()

    register_agents()

    logger.info(
        "Scout backend started successfully.",
    )

    yield

    logger.info(
        "Shutting down Scout backend.",
    )

# ==========================================================
# FastAPI Application
# ==========================================================

app = FastAPI(
    title="Scout API",
    description=(
        "AI-powered disaster education assistance "
        "platform."
    ),
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    chat_router,
    prefix="/api",
    tags=["Chat"],
)
# ==========================================================
# Routers
# ==========================================================

# Example:
#
# from backend.api.chat import router as chat_router
#
# app.include_router(
#     chat_router,
#     prefix="/api",
#     tags=["Chat"],
# )
#
# Uncomment after the chat router is implemented.


# ==========================================================
# Health Check
# ==========================================================

@app.get(
    "/health",
    tags=["Health"],
)
async def health() -> dict[str, str]:
    """
    Health check endpoint.
    """

    return {
        "status": "healthy",
        "service": "Scout Backend",
    }


# ==========================================================
# Root Endpoint
# ==========================================================

@app.get(
    "/",
    tags=["Root"],
)
async def root() -> dict[str, str]:
    """
    Root endpoint.
    """

    return {
        "message": (
            "Welcome to the Scout API."
        ),
    }