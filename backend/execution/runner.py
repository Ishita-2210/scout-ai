"""
Scout Runner.

Provides the execution layer for all Scout conversations.
"""

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from backend.agents.root_agent import create_root_agent


class ScoutRunner:
    """
    Central execution engine for Scout.

    This class is responsible for:

    - Managing ADK sessions
    - Executing the Root Agent
    - Returning the final assistant response
    """

    def __init__(self):

        self.app_name = "scout"

        self.agent = create_root_agent()

        self.session_service = InMemorySessionService()

        self.runner = Runner(
            app_name=self.app_name,
            agent=self.agent,
            session_service=self.session_service,
        )
        
    async def _ensure_session(
        self,
        user_id: str,
        session_id: str,
    ) -> None:
        """
        Ensure that the requested session exists.
        """

        session = await self.session_service.get_session(
            app_name=self.app_name,
            user_id=user_id,
            session_id=session_id,
        )

        if session is None:

            await self.session_service.create_session(
                app_name=self.app_name,
                user_id=user_id,
                session_id=session_id,
            )

    async def chat(
        self,
        user_id: str,
        session_id: str,
        message: str,
    ) -> str:
        """
        Execute a conversation turn.

        Returns
        -------
        str
            Assistant response.
        """

        await self._ensure_session(
            user_id=user_id,
            session_id=session_id,
        )

        content = types.Content(
            role="user",
            parts=[
                types.Part(text=message),
            ],
        )

        assistant_response = ""

        async for event in self.runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content,
        ):

            if event.content is None:
                continue

            if event.content.role != "model":
                continue

            texts = [
                part.text
                for part in event.content.parts
                if getattr(part, "text", None)
            ]

            if texts:
                assistant_response = "".join(texts)

        if not assistant_response:

            raise RuntimeError(
                "Scout returned an empty response."
            )

        return assistant_response