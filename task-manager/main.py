import asyncio
from pathlib import Path

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import root_agent


APP_NAME = "task_manager_app"
USER_ID = "user_1"
SESSION_ID = "session_001"


async def call_agent_async(query: str, runner: Runner) -> None:
    """Send a query to the task manager and print its response."""

    print(f"\nUser: {query}")

    message = types.Content(
        role="user",
        parts=[types.Part(text=query)],
    )

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=message,
    ):
        if not event.content or not event.content.parts:
            continue

        for part in event.content.parts:
            if part.function_call:
                print(f"[Tool Call] {part.function_call.name}({part.function_call.args})")

            elif part.function_response:
                print(f"[Tool Result] {part.function_response.name}: {part.function_response.response}")
            
            elif part.text and part.thought:
                print(f"[Thought] {part.text}")

            elif part.text and event.is_final_response():
                print(f"Agent: {part.text}")


async def main():
    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state={
            "tasks": [],
            "next_task_id": 1,
        },
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    queries = [
        "Add a task to finish the authentication API.",
        "Also add unit tests for the authentication API.",
        "Show me all my tasks.",
        "Mark the first task as completed.",
        "What's still pending?",
    ]

    for query in queries:
        await call_agent_async(query, runner)

        session = await session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID,
        )

        print(f"[State] {session.state}")


if __name__ == "__main__":
    asyncio.run(main())
