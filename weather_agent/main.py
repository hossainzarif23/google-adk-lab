import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import root_agent


APP_NAME = "weather_tutorial_app"
USER_ID = "user_1"
SESSION_ID = "session_001"


async def call_agent_async(query: str, runner: Runner):
    """Send a query to the agent and print its final response."""
    print(f"\nUser: {query}")

    message = types.Content(
        role="user",
        parts=[types.Part(text=query)],
    )

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=message
    ):
        print(f"[Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")
        if event.is_final_response():
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(f"Agent: {part.text}")
            elif event.actions and event.actions.escalate:
                print(f"Agent escalated: {event.error_message or 'No specific message.'}")


async def main():
    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    await call_agent_async("What is the weather in New York?", runner)
    await call_agent_async("How about Paris?", runner)


if __name__ == "__main__":
    asyncio.run(main())
