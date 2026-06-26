import asyncio

from backend.execution.runner import ScoutRunner


USER_ID = "demo-user"
SESSION_ID = "demo-session"


async def main():
    print("=" * 60)
    print("🚀 Starting Scout Runner Test")
    print("=" * 60)

    runner = ScoutRunner()

    print("\nRunner initialized successfully.")

    print("\nCreating session...")

    await runner.create_session(
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    print("Session created.")

    print("\nSending message...\n")

    response = await runner.chat(
        user_id=USER_ID,
        session_id=SESSION_ID,
        message="Hello! Introduce yourself in one paragraph.",
    )

    print("=" * 60)
    print("🤖 Scout Response")
    print("=" * 60)

    print(response)

    print("\nTest completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())