"""Owned conversation APIs with durable request deduplication."""

import asyncio
import hashlib
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError

from backend import config
from backend.api.security import check_origin, identity, issue_identity, limiter
from backend.database import SessionLocal
from backend.database.models import ChatRequestRecord, Conversation, Memory, Message, User
from backend.execution.provider import get_runner
from backend.repositories.conversation import conversation_repository as repo
from backend.schemas.assistant import AssistantResult
from backend.schemas.chat import ChatRequest, ChatResponse
from backend.services.ai_service import AIError

router = APIRouter(dependencies=[Depends(check_origin)])
logger = logging.getLogger(__name__)
active_users: set[str] = set()


def owned_conversation(db, owner, session_id):
    conversation = db.scalar(
        select(Conversation)
        .join(User)
        .where(User.external_id == owner, Conversation.session_id == str(session_id))
    )
    if not conversation:
        raise HTTPException(404, "Conversation not found.")
    return conversation


@router.post("/session")
async def session(request: Request, response: Response):
    limiter.check("session:" + (request.client.host if request.client else "unknown"), 30)
    issue_identity(request, response)
    response.headers["Cache-Control"] = "no-store"
    return {"ready": bool(config.GROQ_API_KEY), "search_available": bool(config.SERPER_API_KEY)}


@router.get("/conversations")
async def conversations(owner: str = Depends(identity)):
    with SessionLocal() as db:
        rows = db.scalars(
            select(Conversation)
            .join(User)
            .where(User.external_id == owner)
            .order_by(Conversation.updated_at.desc())
            .limit(50)
        )
        return [
            {
                "id": c.session_id,
                "title": c.title or "Untitled conversation",
                "updated_at": c.updated_at.isoformat(),
            }
            for c in rows
        ]


@router.get("/conversations/{session_id}")
async def messages(session_id: UUID, owner: str = Depends(identity)):
    with SessionLocal() as db:
        conversation = owned_conversation(db, owner, session_id)
        rows = list(
            db.scalars(
                select(Message)
                .where(Message.conversation_id == conversation.id)
                .order_by(Message.created_at.desc(), Message.id.desc())
                .limit(100)
            )
        )
        result = []
        for row in reversed(rows):
            content = row.content
            if row.role == "assistant":
                # Persist the full public result, while old text messages remain readable.
                record = db.scalar(
                    select(ChatRequestRecord).where(
                        ChatRequestRecord.owner == owner, ChatRequestRecord.id == row.agent_name
                    )
                )
                content = record.result if record and record.result else {"text": content}
            result.append({"id": row.id, "role": row.role, "content": content})
        return result


@router.delete("/conversations/{session_id}", status_code=204)
async def delete_conversation(session_id: UUID, owner: str = Depends(identity)):
    if owner in active_users:
        raise HTTPException(409, "Wait for your current answer before deleting a conversation.")
    with SessionLocal() as db:
        conversation = owned_conversation(db, owner, session_id)
        record_ids = list(
            db.scalars(
                select(Message.agent_name).where(
                    Message.conversation_id == conversation.id, Message.role == "assistant"
                )
            )
        )
        db.execute(
            update(ChatRequestRecord)
            .where(ChatRequestRecord.owner == owner, ChatRequestRecord.id.in_([r for r in record_ids if r]))
            .values(result=None, status="deleted")
        )
        # SQLite foreign-key enforcement varies in old installations; delete explicitly.
        db.execute(delete(Message).where(Message.conversation_id == conversation.id))
        db.delete(conversation)
        db.commit()
    return Response(status_code=204)


async def run_connected(request: Request, operation):
    """Cancel pending provider work when the browser disconnects."""
    task = asyncio.create_task(operation)
    try:
        while not task.done():
            if await request.is_disconnected():
                raise asyncio.CancelledError
            await asyncio.wait({task}, timeout=0.25)
        return await task
    finally:
        if not task.done():
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)


@router.delete("/data", status_code=204)
async def delete_all_data(owner: str = Depends(identity)):
    if owner in active_users:
        raise HTTPException(409, "Wait for your current answer before deleting your data.")
    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.external_id == owner))
        if user:
            ids = select(Conversation.id).where(Conversation.user_id == user.id)
            db.execute(delete(Message).where(Message.conversation_id.in_(ids)))
            db.execute(delete(Conversation).where(Conversation.user_id == user.id))
            db.execute(delete(Memory).where(Memory.user_id == user.id))
            db.delete(user)
        db.execute(delete(ChatRequestRecord).where(ChatRequestRecord.owner == owner))
        db.commit()
    return Response(status_code=204)


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, request: Request, owner: str = Depends(identity)):
    key = str(payload.request_id)
    digest = hashlib.sha256(f"{payload.session_id}:{payload.message}".encode()).hexdigest()
    with SessionLocal() as db:
        record = db.scalar(
            select(ChatRequestRecord).where(
                ChatRequestRecord.owner == owner, ChatRequestRecord.request_id == key
            )
        )
        if record:
            if record.payload_hash != digest:
                raise HTTPException(409, "This request ID was already used for a different message.")
            if record.status == "complete":
                return ChatResponse(response=AssistantResult.model_validate(record.result), request_id=key)
            raise HTTPException(
                409,
                "This request is already processing or was interrupted. Check conversation history before sending again.",
            )
    if owner in active_users or len(active_users) >= 8:
        raise HTTPException(409, "An answer is already being prepared. Please wait.")
    limiter.check("user:" + owner, config.CHAT_REQUESTS_PER_MINUTE)
    limiter.check(
        "ip:" + (request.client.host if request.client else "unknown"), config.CHAT_REQUESTS_PER_MINUTE * 3
    )
    active_users.add(owner)
    record_id = None
    try:
        with SessionLocal() as db:
            record = ChatRequestRecord(owner=owner, request_id=key, payload_hash=digest)
            db.add(record)
            db.commit()
            record_id = record.id
        try:
            async with asyncio.timeout(config.CHAT_TIMEOUT):
                result = await run_connected(
                    request,
                    get_runner().chat(
                        user_id=owner,
                        session_id=str(payload.session_id),
                        message=payload.message,
                        request_id=request.state.request_id,
                    ),
                )
        except TimeoutError as exc:
            raise AIError(
                "timeout", "Scout took too long to respond. Please try a more specific question.", 504
            ) from exc
        with SessionLocal() as db:
            conversation = repo.get_or_create_conversation(
                session=db,
                external_user_id=owner,
                session_id=str(payload.session_id),
                title=payload.message[:80],
            )
            repo.create_message(session=db, conversation=conversation, role="user", content=payload.message)
            repo.create_message(
                session=db,
                conversation=conversation,
                role="assistant",
                content=result.text,
                agent_name=record_id,
            )
            from datetime import datetime, timezone

            conversation.updated_at = datetime.now(timezone.utc)
            record = db.get(ChatRequestRecord, record_id)
            record.status, record.result = "complete", result.model_dump()
            db.commit()
        return ChatResponse(response=result, request_id=key)
    except IntegrityError:
        raise HTTPException(409, "This request is already processing.") from None
    except AIError as exc:
        logger.warning(
            "chat request_id=%s category=%s status=%d", request.state.request_id, exc.code, exc.status
        )
        raise HTTPException(
            exc.status,
            {"code": exc.code, "message": exc.message},
            headers={"Retry-After": str(exc.retry_after)} if exc.retry_after else None,
        ) from None
    finally:
        active_users.discard(owner)
        if record_id:
            with SessionLocal() as db:
                record = db.get(ChatRequestRecord, record_id)
                if record and record.status == "running":
                    record.status = "interrupted"
                    db.commit()
