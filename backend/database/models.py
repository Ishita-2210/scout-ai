"""
Scout Database Models.

Defines the SQLAlchemy ORM models used for
persistent storage.
"""
from __future__ import annotations
from sqlalchemy import Float
from datetime import UTC, datetime
from uuid import uuid4
from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from backend.database.base import Base


# ==========================================================
# Shared Mixins
# ==========================================================


class UUIDMixin:
    """
    Provides a UUID primary key.
    """

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )


class TimestampMixin:
    """
    Provides timezone-aware timestamps.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )


# ==========================================================
# User
# ==========================================================


class User(UUIDMixin, TimestampMixin, Base):
    """
    Represents a Scout user.
    """

    __tablename__ = "users"

    external_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    memories: Mapped[list["Memory"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

# ==========================================================
# Conversation
# ==========================================================


class Conversation(UUIDMixin, TimestampMixin, Base):
    """
    Represents a conversation between a user
    and the Scout system.
    """

    __tablename__ = "conversations"

    session_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    title: Mapped[str | None] = mapped_column(
        String(255),
        default=None,
    )

    user: Mapped["User"] = relationship(
        back_populates="conversations",
    )

    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="Message.created_at",
    )

    __table_args__ = (
        Index(
            "ix_conversations_user_session",
            "user_id",
            "session_id",
        ),
    )


# ==========================================================
# Message
# ==========================================================


class Message(UUIDMixin, TimestampMixin, Base):
    """
    Represents a single message exchanged
    during a conversation.
    """

    __tablename__ = "messages"

    conversation_id: Mapped[str] = mapped_column(
        ForeignKey(
            "conversations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    agent_name: Mapped[str | None] = mapped_column(
        String(100),
        default=None,
    )

    conversation: Mapped["Conversation"] = relationship(
        back_populates="messages",
    )

    __table_args__ = (
        Index(
            "ix_messages_conversation_created",
            "conversation_id",
            "created_at",
        ),
        Index(
            "ix_messages_role",
            "role",
        ),
    )

# ==========================================================
# Memory
# ==========================================================


class Memory(UUIDMixin, TimestampMixin, Base):
    """
    Represents long-term memory extracted from
    user conversations.
    """

    __tablename__ = "memories"

    user_id: Mapped[str] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    key: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    value: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=lambda: {},
    )

    category: Mapped[str] = mapped_column(
        String(50),
        default="general",
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        default=1.0,
        nullable=False,
    )
    source: Mapped[str | None] = mapped_column(
        String(100),
        default=None,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="memories",
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "key",
            name="uq_memories_user_key",
        ),
        Index(
            "ix_memories_user_key",
            "user_id",
            "key",
        ),
        Index(
            "ix_memories_category",
            "category",
        ),
    )

__all__ = (
    "UUIDMixin",
    "TimestampMixin",
    "User",
    "Conversation",
    "Message",
    "Memory",
)
