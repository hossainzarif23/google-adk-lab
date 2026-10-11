import asyncio
from pathlib import Path

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import root_agent


APP_NAME = "code_review_team_app"
USER_ID = "user_1"


async def call_agent_async(
    query: str,
    runner: Runner,
    session_id: str,
) -> None:
    """Send a query to the agent team and print execution events."""
    print(f"\nUser: {query}\n")

    message = types.Content(
        role="user",
        parts=[types.Part(text=query)],
    )

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=message,
    ):
        if event.actions and event.actions.transfer_to_agent:
            print(f"[Delegation] {event.author} -> {event.actions.transfer_to_agent}")

        if not event.content or not event.content.parts:
            if event.is_final_response() and event.actions and event.actions.escalate:
                print(f"[Escalated] {event.error_message or 'No specific message.'}")
            continue

        for part in event.content.parts:
            if part.function_call:
                call = part.function_call
                print(f"[Tool Call] {event.author}: {call.name}({call.args})")

            elif part.function_response:
                response = part.function_response
                print(f"[Tool Result] {event.author}: {response.name}")

            elif part.text and part.thought:
                print(f"[Thought] {event.author}: {part.text}")

            elif part.text and event.is_final_response():
                print(f"\n[{event.author}]\n{part.text}")

        if event.is_final_response() and event.error_message:
            print(f"[Error] {event.error_message}")


async def main():
    session_service = InMemorySessionService()

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    code = Path(__file__).with_name("sample_code.py").read_text(encoding="utf-8")

    queries = [
        f"Review this Python code for bugs:\n\n{code}",
        f"Generate pytest tests for this Python code:\n\n{code}",
    ]

    for index, query in enumerate(queries, start=1):
        session_id = f"session_{index}"

        await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
        )

        await call_agent_async(
            query=query,
            runner=runner,
            session_id=session_id,
        )


if __name__ == "__main__":
    asyncio.run(main())
