import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select

from backend import config
from backend.database import SessionLocal
from backend.database.models import ChatRequestRecord, Conversation, Memory, Message
from backend.execution.runner import ScoutRunner
from backend.main import app
from backend.memory.models import MemoryUpdate
from backend.schemas.assistant import AssistantResult, RoutePlan, Section, Task
from backend.services.ai_service import AIError


def payload(**changes):
    return {"session_id": str(uuid4()), "request_id": str(uuid4()), "message": "Help with school", **changes}


@pytest.fixture
def mock_runner(monkeypatch):
    result = AssistantResult(
        text="A useful answer",
        sections=[
            Section(
                domain="school",
                title="Schools",
                guidance="A useful answer",
                data={"query": "school", "schools": []},
            )
        ],
    )
    runner = SimpleNamespace(chat=AsyncMock(return_value=result))
    monkeypatch.setattr("backend.api.chat.get_runner", lambda: runner)
    return runner


def test_persist_reload_idempotency_and_ownership(client, mock_runner):
    body = payload()
    response = client.post("/api/chat", json=body)
    assert response.status_code == 200, response.text
    assert response.headers["x-request-id"]
    assert client.post("/api/chat", json=body).json() == response.json()
    assert mock_runner.chat.await_count == 1
    rows = client.get(f"/api/conversations/{body['session_id']}").json()
    assert [r["role"] for r in rows] == ["user", "assistant"]
    assert rows[1]["content"]["sections"][0]["title"] == "Schools"
    assert client.get("/api/conversations").json()[0]["title"] == body["message"]
    assert client.post("/api/chat", json={**body, "message": "changed"}).status_code == 409
    with TestClient(app) as other:
        assert other.get("/api/conversations").status_code == 401
        other.post("/api/session")
        assert other.get(f"/api/conversations/{body['session_id']}").status_code == 404
        assert other.delete(f"/api/conversations/{body['session_id']}").status_code == 404
    with SessionLocal() as db:
        assert db.scalar(select(func.count()).select_from(Message)) == 2


@pytest.mark.parametrize("message", ["", "   ", "a" * 4001])
def test_invalid_message(client, mock_runner, message):
    assert client.post("/api/chat", json=payload(message=message)).status_code == 422
    mock_runner.chat.assert_not_called()


def test_body_size_origin_and_untrusted_user_id(client, mock_runner):
    assert client.post("/api/chat", content=b"x" * 24001).status_code == 413
    assert (
        client.post("/api/chat", json=payload(), headers={"Origin": "https://evil.example"}).status_code
        == 403
    )
    assert client.post("/api/chat", json={**payload(), "user_id": "test_user"}).status_code == 422
    cookie = client.cookies.get("scout_session")
    tampered = cookie[:-1] + ("1" if cookie[-1] == "0" else "0")
    assert (
        client.get("/api/conversations", headers={"Cookie": f"scout_session={tampered}"}).status_code == 401
    )


def test_failure_is_safe_and_not_saved_or_implicitly_replayed(client, mock_runner):
    mock_runner.chat.side_effect = AIError("quota_exhausted", "Daily quota exhausted.", 429, 3600)
    body = payload()
    response = client.post("/api/chat", json=body)
    assert response.status_code == 429 and response.headers["retry-after"] == "3600"
    assert response.json()["detail"]["code"] == "quota_exhausted"
    assert client.post("/api/chat", json=body).status_code == 409
    assert mock_runner.chat.await_count == 1
    with SessionLocal() as db:
        assert db.scalar(select(func.count()).select_from(Message)) == 0


def test_application_rate_limit(client, mock_runner, monkeypatch):
    monkeypatch.setattr(config, "CHAT_REQUESTS_PER_MINUTE", 1)
    assert client.post("/api/chat", json=payload()).status_code == 200
    response = client.post("/api/chat", json=payload())
    assert response.status_code == 429 and int(response.headers["retry-after"]) > 0
    assert mock_runner.chat.await_count == 1


def test_delete_removes_messages_and_response_data(client, mock_runner):
    body = payload()
    client.post("/api/chat", json=body)
    assert client.delete(f"/api/conversations/{body['session_id']}").status_code == 204
    assert client.get("/api/conversations").json() == []
    with SessionLocal() as db:
        assert db.scalar(select(func.count()).select_from(Message)) == 0
        assert db.scalar(select(ChatRequestRecord)).result is None


def test_delete_all_data(client, mock_runner):
    client.post("/api/chat", json=payload())
    assert client.delete("/api/data").status_code == 204
    with SessionLocal() as db:
        for model in (Message, Memory, Conversation, ChatRequestRecord):
            assert db.scalar(select(func.count()).select_from(model)) == 0


def test_unexpected_failure_does_not_expose_internal_details(client, mock_runner):
    mock_runner.chat.side_effect = RuntimeError("private internal error and credentials")
    response = client.post("/api/chat", json=payload())
    assert response.status_code == 500
    assert "private" not in response.text and "credentials" not in response.text


def test_overall_turn_timeout(client, mock_runner, monkeypatch):
    async def slow(**kwargs):
        await asyncio.sleep(1)

    mock_runner.chat.side_effect = slow
    monkeypatch.setattr(config, "CHAT_TIMEOUT", 0.01)
    response = client.post("/api/chat", json=payload())
    assert response.status_code == 504
    assert response.json()["detail"]["code"] == "timeout"


def test_full_orchestration_calls_every_selected_specialist(client, monkeypatch):
    calls = []

    async def complete(messages, schema, request_id):
        calls.append(schema.__name__)
        if schema is RoutePlan:
            return RoutePlan(
                tasks=[
                    Task(domain=d)
                    for d in ("school", "document", "scholarship", "housing", "legal", "counselling")
                ],
                profile=MemoryUpdate(grade="8"),
            )
        data = {
            "SchoolAnswer": {"query": "q", "schools": []},
            "DocumentAnswer": {"query": "q", "documents": []},
            "ScholarshipAnswer": {"query": "q", "scholarships": []},
            "HousingAnswer": {"query": "q", "housing": []},
            "LegalAnswer": {"query": "q", "resources": []},
            "CounsellingAnswer": {
                "guidance": "Take one small step",
                "recommendations": ["Start a short study session"],
            },
        }
        return schema.model_validate({"guidance": "Practical next steps", "data": data[schema.__name__]})

    monkeypatch.setattr("backend.execution.runner.ai_service.complete", complete)
    monkeypatch.setattr(
        "backend.execution.runner.retrieve", lambda *args: ("Reference", ["guide.pdf, page 1"])
    )
    body = payload()
    result = client.post("/api/chat", json=body)
    assert result.status_code == 200, result.text
    assert len(result.json()["response"]["sections"]) == 6
    assert len(calls) == 7
    with SessionLocal() as db:
        owner = db.scalar(select(ChatRequestRecord.owner))
        assert db.scalar(select(Memory)).value == {"value": "8"}
    history = ScoutRunner().history(owner, body["session_id"])
    assert [m["role"] for m in history] == ["user", "assistant"]
    assert ScoutRunner().history(str(uuid4()), body["session_id"]) == []


def test_disconnect_cancels_operation():
    from backend.api.chat import run_connected

    cancelled = []

    async def operation():
        try:
            await asyncio.sleep(100)
        finally:
            cancelled.append(True)

    async def disconnected():
        await asyncio.sleep(0)
        return True

    async def run():
        with pytest.raises(asyncio.CancelledError):
            await run_connected(SimpleNamespace(is_disconnected=disconnected), operation())

    asyncio.run(run())
    assert cancelled == [True]
