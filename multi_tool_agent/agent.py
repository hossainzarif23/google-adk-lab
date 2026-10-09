from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import requests
from google.adk.agents import Agent

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

def get_coordinates(city: str) -> dict:
    response = requests.get(
        GEOCODING_URL,
        params={"name": city, "count": 1},
        timeout=10,
    )
    response.raise_for_status()

    locations = response.json().get("results", [])

    if not locations:
        raise ValueError(f"City '{city}' not found.")

    return locations[0]


def get_weather(city: str) -> dict:
    """Retrieve the current weather conditions for a city worldwide.

    Args:
        city: Name of the city, optionally including country.

    Returns:
        A dictionary containing status and weather information,
        or an error message if the request fails.
    """
    try:
        location = get_coordinates(city)

        response = requests.get(
            WEATHER_URL,
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": ",".join(
                    [
                        "temperature_2m",
                        "relative_humidity_2m",
                        "apparent_temperature",
                        "precipitation",
                        "weather_code",
                        "wind_speed_10m",
                    ]
                )
            },
            timeout=10,
        )
        response.raise_for_status()

        weather = response.json()["current"]

        return {
            "status": "success",
            "city": location["name"],
            "country": location["country"],
            "weather": weather
        }

    except (requests.RequestException, ValueError, KeyError) as exc:
        return {
            "status": "error",
            "error_message": str(exc),
        }


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
    name="weather_time_agent",
    model="gemini-3.5-flash",
    description=(
        "An agent that provides current weather conditions "
        "and local time information for cities worldwide."
    ),
    instruction=(
        "You are a helpful assistant that provides current weather "
        "and local time information for cities worldwide. "
        "For weather-related questions, use the get_weather tool "
        "with the requested city name. "
        "For time-related questions, determine the appropriate IANA "
        "timezone (e.g., Asia/Dhaka or Europe/London) and use the "
        "get_current_time tool. "
        "If the user asks about both weather and time, use both tools. "
        "Always use tool results to answer questions. "
        "Never invent weather conditions or current times. "
        "If a tool returns an error, explain it clearly to the user."
    ),
    tools=[get_weather, get_current_time],
)
