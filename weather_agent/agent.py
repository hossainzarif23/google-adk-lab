from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import requests
from dotenv import load_dotenv
from typing import Literal


load_dotenv()  # Load environment variables from .env file


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
        A dictionary containing status, location, weather data,
        and measurement units, or an error message if the request fails.
    """
    try:
        location = get_coordinates(city)

        response = requests.get(
            WEATHER_URL,
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "temperature_unit": "celsius",
                "wind_speed_unit": "kmh",
                "precipitation_unit": "mm",
                "current": ",".join(
                    [
                        "temperature_2m",
                        "relative_humidity_2m",
                        "apparent_temperature",
                        "precipitation",
                        "weather_code",
                        "wind_speed_10m",
                    ]
                ),
            },
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()

        return {
            "status": "success",
            "city": location["name"],
            "country": location["country"],
            "weather": data["current"],
            "units": data["current_units"],
        }

    except (requests.RequestException, ValueError, KeyError) as exc:
        return {
            "status": "error",
            "error_message": str(exc),
        }


def get_agent(provider: Literal["gemini", "mimo"]) -> Agent:
    return Agent(
        name=f"weather_agent_{provider}",
        model=(
            "gemini-3.5-flash"
            if provider == "gemini"
            else LiteLlm(model="xiaomi_mimo/mimo-v2.6-flash")
        ),
        description="Provides current weather information for cities.",
        instruction=(
            "You are a helpful weather assistant. "
            "When the user asks about the weather in a city, "
            "use the get_weather tool. "
            "Present the results clearly and explain any tool errors."
        ),
        tools=[get_weather],
    )
