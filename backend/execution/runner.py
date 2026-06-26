from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from backend.agents.root_agent import create_root_agent


class ScoutRunner:
    """
    Central execution engine for Scout.
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

    async def create_session(
        self,
        user_id: str,
        session_id: str,
    ):

        return await self.session_service.create_session(
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

        content = types.Content(
            role="user",
            parts=[
                types.Part(text=message)
            ],
        )

        response = ""

        async for event in self.runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content,
        ):

            if (
                event.content
                and event.content.parts
                and event.content.role == "model"
            ):

                response = "".join(
                    part.text
                    for part in event.content.parts
                    if hasattr(part, "text")
                    and part.text
                )

        return response