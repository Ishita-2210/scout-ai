"""
Scout Database Session.

Creates the SQLAlchemy engine and session factory
used throughout the Scout backend.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from backend.config import DATABASE_URL


# ==========================================================
# Engine
# ==========================================================

_ENGINE_OPTIONS = {
    "future": True,
    "echo": False,
}


# SQLite requires check_same_thread=False
if DATABASE_URL.startswith("sqlite"):

    _ENGINE_OPTIONS["connect_args"] = {
        "check_same_thread": False,
    }


engine: Engine = create_engine(
    DATABASE_URL,
    **_ENGINE_OPTIONS,
)


# ==========================================================
# Session Factory
# ==========================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
)


# ==========================================================
# Session Dependency
# ==========================================================

def get_session() -> Generator[Session, None, None]:
    """
    Provide a transactional database session.

    Yields
    ------
    Session
        SQLAlchemy session.
    """

    session = SessionLocal()

    try:
        yield session

    finally:
        session.close()


# ==========================================================
# Utilities
# ==========================================================

def create_tables() -> None:
    """
    Create all registered database tables.

    Intended for development only.
    """

    from backend.database.base import Base

    Base.metadata.create_all(
        bind=engine,
    )


__all__ = (
    "engine",
    "SessionLocal",
    "get_session",
    "create_tables",
)