"""
Scout Runner.

Executes conversations through the Scout
multi-agent system.
"""

from __future__ import annotations

import logging
from typing import Any
from typing import Final

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from backend.agents.registry import registry

from backend.agents.root.constants import (
    AGENT_NAME as ROOT_AGENT_NAME,
)

from backend.database import (
    SessionLocal,
)

from backend.memory.service import (
    memory_service,
)

from backend.repositories.conversation import (
    conversation_repository,
)

APP_NAME: Final = "scout"

logger = logging.getLogger(__name__)


# ==========================================================
# Scout Runner
# ==========================================================


class ScoutRunner:
    """
    Executes Scout conversations.

    Responsibilities
    ----------------
    • Manage ADK sessions
    • Persist conversations
    • Inject long-term memory
    • Execute the Root Agent
    • Update memory
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize the Scout runner.
        """

        self.app_name = APP_NAME

        if ROOT_AGENT_NAME not in registry:

            raise RuntimeError(
                "Root Agent has not been registered."
            )

        self.agent = registry.get(
            ROOT_AGENT_NAME,
        )

        self.session_service = (
            InMemorySessionService()
        )

        self.runner = Runner(
            app_name=self.app_name,
            agent=self.agent,
            session_service=self.session_service,
        )

    # ======================================================
    # Session Management
    # ======================================================

    async def _ensure_session(
        self,
        *,
        user_id: str,
        session_id: str,
    ) -> None:
        """
        Ensure an ADK session exists.
        """

        session = (
            await self.session_service.get_session(
                app_name=self.app_name,
                user_id=user_id,
                session_id=session_id,
            )
        )

        if session is not None:
            return

        logger.info(
            "Creating ADK session '%s'.",
            session_id,
        )

        await self.session_service.create_session(
            app_name=self.app_name,
            user_id=user_id,
            session_id=session_id,
        )

    # ======================================================
    # Database Helpers
    # ======================================================

    @staticmethod
    def _get_conversation(
        *,
        db,
        user_id: str,
        session_id: str,
    ):
        """
        Retrieve or create a conversation.
        """

        return (
            conversation_repository.get_or_create_conversation(
                session=db,
                external_user_id=user_id,
                session_id=session_id,
            )
        )

    @staticmethod
    def _save_message(
        *,
        db,
        conversation,
        role: str,
        content: str,
        agent_name: str | None = None,
    ) -> None:
        """
        Persist a conversation message.
        """

        conversation_repository.create_message(
            session=db,
            conversation=conversation,
            role=role,
            content=content,
            agent_name=agent_name,
        )

    # ======================================================
    # Prompt Construction
    # ======================================================

    @staticmethod
    def _build_content(
        *,
        memory_context: str,
        message: str,
    ) -> types.Content:
        """
        Build the prompt sent to the Root Agent.
        """

        if memory_context:

            prompt = (
                f"{memory_context}\n\n"
                f"User Message:\n"
                f"{message}"
            )

        else:

            prompt = message

        return types.Content(
            role="user",
            parts=[
                types.Part(
                    text=prompt,
                ),
            ],
        )

    # ======================================================
    # Response Extraction
    # ======================================================

    @staticmethod
    def _extract_response(
        event: Any,
    ) -> str:
        """
        Extract assistant text from
        an ADK event.
        """

        content = getattr(
            event,
            "content",
            None,
        )

        if content is None:
            return ""

        if content.role != "model":
            return ""

        texts = [
            part.text
            for part in content.parts
            if getattr(
                part,
                "text",
                None,
            )
        ]

        return "".join(
            texts,
        )
    # ======================================================
    # Conversation Execution
    # ======================================================

    async def chat(
        self,
        *,
        user_id: str,
        session_id: str,
        message: str,
    ) -> str:
        """
        Execute a single conversation turn.
        """

        logger.info(
            "Processing request for user '%s'.",
            user_id,
        )

        await self._ensure_session(
            user_id=user_id,
            session_id=session_id,
        )

        # --------------------------------------------------
        # Load Memory
        # --------------------------------------------------

        memory_context = memory_service.build_context(
            user_id=user_id,
        )

        # --------------------------------------------------
        # RAG Hook
        # --------------------------------------------------

        # Future integration:
        #
        # rag_context = rag_service.retrieve_context(
        #     query=message,
        # )
        #
        # memory_context = (
        #     f"{memory_context}\n\n"
        #     f"{rag_context}"
        # )

        # --------------------------------------------------
        # Build Prompt
        # --------------------------------------------------

        content = self._build_content(
            memory_context=memory_context,
            message=message,
        )

        # --------------------------------------------------
        # Persist User Message
        # --------------------------------------------------

        with SessionLocal() as db:

            conversation = self._get_conversation(
                db=db,
                user_id=user_id,
                session_id=session_id,
            )

            self._save_message(
                db=db,
                conversation=conversation,
                role="user",
                content=message,
            )

            db.commit()

        # --------------------------------------------------
        # Execute Root Agent
        # --------------------------------------------------

        assistant_response = ""

        try:

            async for event in self.runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=content,
            ):

                response = self._extract_response(
                    event,
                )

                if response:

                    assistant_response = response

        except Exception:

            logger.exception(
                "Runner execution failed.",
            )

            raise

        if not assistant_response:

            raise RuntimeError(
                "Scout returned an empty response."
            )

        # --------------------------------------------------
        # Persist Assistant Message
        # --------------------------------------------------

        with SessionLocal() as db:

            conversation = self._get_conversation(
                db=db,
                user_id=user_id,
                session_id=session_id,
            )

            self._save_message(
                db=db,
                conversation=conversation,
                role="assistant",
                content=assistant_response,
                agent_name=ROOT_AGENT_NAME,
            )

            db.commit()

        # --------------------------------------------------
        # Update Long-Term Memory
        # --------------------------------------------------

        try:

            memory_service.update_from_message(
                user_id=user_id,
                message=message,
            )

        except Exception:

            logger.exception(
                "Failed to update user memory.",
            )

        logger.info(
            "Completed request for user '%s'.",
            user_id,
        )

        return assistant_response


__all__ = (
    "ScoutRunner",
)