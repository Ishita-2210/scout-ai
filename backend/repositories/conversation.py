"""
Scout Conversation Repository.

Provides database operations for users,
conversations, and messages.

Transaction management is intentionally left
to the caller.
"""

from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database.models import (
    Conversation,
    Message,
    User,
)

logger = logging.getLogger(__name__)


class ConversationRepository:
    """
    Repository for conversation persistence.

    This repository performs CRUD operations
    only. Transactions are managed by the
    service layer.
    """

    # ======================================================
    # User Operations
    # ======================================================

    def get_user(
        self,
        session: Session,
        external_id: str,
    ) -> User | None:
        """
        Retrieve a user by external identifier.
        """

        return session.scalar(
            select(User).where(
                User.external_id == external_id,
            )
        )

    def create_user(
        self,
        session: Session,
        external_id: str,
    ) -> User:
        """
        Create a new Scout user.
        """

        user = User(
            external_id=external_id,
        )

        session.add(user)

        session.flush()

        logger.info(
            "Created user '%s'.",
            external_id,
        )

        return user

    def get_or_create_user(
        self,
        session: Session,
        external_id: str,
    ) -> User:
        """
        Retrieve an existing user or create one.
        """

        user = self.get_user(
            session,
            external_id,
        )

        if user is not None:
            return user

        return self.create_user(
            session,
            external_id,
        )

    # ======================================================
    # Conversation Operations
    # ======================================================

    def get_conversation(
        self,
        session: Session,
        *,
        user: User,
        session_id: str,
    ) -> Conversation | None:
        """
        Retrieve a conversation.
        """

        return session.scalar(
            select(Conversation).where(
                Conversation.user_id == user.id,
                Conversation.session_id == session_id,
            )
        )

    def create_conversation(
        self,
        session: Session,
        *,
        user: User,
        session_id: str,
        title: str | None = None,
    ) -> Conversation:
        """
        Create a new conversation.
        """

        conversation = Conversation(
            user_id=user.id,
            session_id=session_id,
            title=title,
        )

        session.add(
            conversation,
        )

        session.flush()

        logger.info(
            "Created conversation '%s'.",
            session_id,
        )

        return conversation

    def get_or_create_conversation(
        self,
        session: Session,
        *,
        external_user_id: str,
        session_id: str,
        title: str | None = None,
    ) -> Conversation:
        """
        Retrieve an existing conversation or create one.
        """

        user = self.get_or_create_user(
            session=session,
            external_id=external_user_id,
        )

        conversation = self.get_conversation(
            session=session,
            user=user,
            session_id=session_id,
        )

        if conversation is not None:
            return conversation

        return self.create_conversation(
            session=session,
            user=user,
            session_id=session_id,
            title=title,
        )

    # ======================================================
    # Message Operations
    # ======================================================

    def create_message(
        self,
        session: Session,
        *,
        conversation: Conversation,
        role: str,
        content: str,
        agent_name: str | None = None,
    ) -> Message:
        """
        Persist a conversation message.
        """

        message = Message(
            conversation_id=conversation.id,
            role=role,
            content=content,
            agent_name=agent_name,
        )

        session.add(
            message,
        )

        session.flush()

        return message

    def list_messages(
        self,
        session: Session,
        conversation: Conversation,
    ) -> list[Message]:
        """
        Return all messages belonging to a conversation.
        """

        return list(
            session.scalars(
                select(Message)
                .where(
                    Message.conversation_id == conversation.id,
                )
                .order_by(
                    Message.created_at.asc(),
                )
            )
        )

    # ======================================================
    # Delete Operations
    # ======================================================

    def delete_conversation(
        self,
        session: Session,
        conversation: Conversation,
    ) -> None:
        """
        Delete a conversation.
        """

        session.delete(
            conversation,
        )

        logger.info(
            "Deleted conversation '%s'.",
            conversation.session_id,
        )


conversation_repository = ConversationRepository()


__all__ = (
    "ConversationRepository",
    "conversation_repository",
)