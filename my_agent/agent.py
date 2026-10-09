from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from google.adk.agents.llm_agent import Agent


def get_current_time(timezone: str) -> dict:
    """Returns the current time in an IANA timezone.
    Args:
        timezone: IANA timezone, such as Asia/Dhaka
            or Europe/London.
    """
    try:
        current_time = datetime.now(ZoneInfo(timezone))

        return {
            "status": "success",
            "timezone": timezone,
            "time": current_time.isoformat(),
        }
    except ZoneInfoNotFoundError:
        return {
            "status": "error",
            "message": f"Unknown timezone: {timezone}",
        }


root_agent = Agent(
    model="gemini-3.5-flash",
    name="root_agent",
    description="Tells the current time in cities.",
    instruction=(
        "You are a helpful assistant that tells the current "
        "time in cities. Determine the city's IANA timezone "
        "and call get_current_time. Never invent the time."
    ),
    tools=[get_current_time],
)
