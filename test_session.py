import asyncio

from google.adk.sessions import InMemorySessionService


async def main():

    service = InMemorySessionService()

    session = await service.get_session(
        app_name="scout",
        user_id="ishita",
        session_id="session-1",
    )

    print(session)


asyncio.run(main())