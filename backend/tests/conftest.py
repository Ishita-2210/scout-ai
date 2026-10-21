"""Tests always use an isolated database and never read or mutate scout.db."""

import os
import tempfile
from pathlib import Path

os.environ["DATABASE_URL"] = (
    "sqlite:///" + (Path(tempfile.mkdtemp(prefix="scout-tests-")) / "test.db").as_posix()
)
os.environ["GROQ_API_KEY"] = "test-key-never-sent"
os.environ["SESSION_SECRET"] = "test-session-secret-" * 4
os.environ["SERPER_API_KEY"] = ""

import pytest
from fastapi.testclient import TestClient

from backend.api.chat import active_users
from backend.api.security import limiter
from backend.database import Base, engine
from backend.main import app


@pytest.fixture(autouse=True)
def isolated_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    limiter.buckets.clear()
    active_users.clear()
    yield


@pytest.fixture
def client():
    with TestClient(app) as client:
        client.post("/api/session")
        yield client
