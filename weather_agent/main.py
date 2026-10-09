import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from typing import Literal

from agent import get_agent


APP_NAME = "weather_tutorial_app"
USER_ID = "user_1"
SESSION_ID = "session_001"


async def call_agent_async(query: str, runner: Runner) -> None:
    """Send a query to the agent and log its execution."""

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
            if event.is_final_response() and event.actions and event.actions.escalate:
                print(f"[Escalated] {event.error_message or 'No specific message.'}")
            continue

        for part in event.content.parts:
            if part.function_call:
                call = part.function_call
                print(f"[Tool Call] {call.name}({call.args})")

            elif part.function_response:
                response = part.function_response
                print(f"[Tool Result] {response.name}: {response.response}")

            elif part.text and part.thought:
                print(f"[Thought] {part.text}")

            elif part.text and event.is_final_response():
                print(f"\nAgent: {part.text}")

        if event.is_final_response() and event.actions and event.actions.escalate:
            print(f"[Escalated] {event.error_message or 'No specific message.'}")


async def main(provider: Literal["gemini", "mimo"]):
    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    runner = Runner(
        agent=get_agent(provider),
        app_name=APP_NAME,
        session_service=session_service
    )
    await call_agent_async("Compare the weather in New York, Paris, and Tokyo. Which city has the best weather for walking outdoors?", runner)


async def run_comparison():
    await main("mimo")
    await main("gemini")


if __name__ == "__main__":
    asyncio.run(run_comparison())
