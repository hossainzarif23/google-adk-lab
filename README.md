# Google ADK Python Learning Lab

This repository contains two small agents built with Google's [Agent Development Kit (ADK) for Python](https://adk.dev/get-started/python/): a timezone lookup quickstart and a multi-tool weather and time assistant.

## Agents

### `my_agent` — timezone lookup

`my_agent/agent.py` defines `root_agent` and the `get_current_time` tool. The assistant determines a city's IANA timezone and returns its current time in ISO 8601 format. Examples of timezone names include `Asia/Dhaka` and `Europe/London`.

### `multi_tool_agent` — weather and local time

`multi_tool_agent/agent.py` defines `weather_time_agent` with two tools:

- `get_weather` looks up a city with the Open-Meteo geocoding API, then retrieves current temperature, humidity, apparent temperature, precipitation, weather code, and wind speed from Open-Meteo.
- `get_current_time` returns the current time for an IANA timezone.

The assistant can answer weather questions, time questions, or both. Weather lookup uses the first geocoding result, so include a country when a city name could refer to more than one place. Open-Meteo access requires an internet connection and no API key for this example.

## Requirements

- Python 3.10 or newer
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)
- An internet connection for Gemini and Open-Meteo requests

## Set up

Run these commands from the repository root. They create a local virtual environment and install ADK plus the `requests` dependency used by `multi_tool_agent`.

### Windows PowerShell

```powershell
uv venv
.venv\Scripts\Activate.ps1
uv pip install google-adk requests
```

### macOS or Linux

```bash
uv venv
source .venv/bin/activate
uv pip install google-adk requests
```

Create an `.env` file inside the folder for the agent you want to run, such as `my_agent/.env` or `multi_tool_agent/.env`, and add your Gemini API key:

```dotenv
GOOGLE_API_KEY="your-api-key"
```

Keep the key private. The repository's `.gitignore` excludes `.env` files and local ADK session data.

## Run an agent

With the virtual environment activated, start either agent from the repository root:

```bash
adk run my_agent
```

```bash
adk run multi_tool_agent
```

To use ADK's local development chat interface instead, run:

```bash
adk web --port 8000
```

Open <http://localhost:8000> and select `my_agent` or `multi_tool_agent`. ADK Web is intended for development and debugging, not production use.

Example questions:

- `my_agent`: “What time is it in Dhaka?”
- `multi_tool_agent`: “What is the current weather and local time in London?”

## Learn more

- [ADK Python quickstart](https://adk.dev/get-started/python/)
- [ADK documentation](https://google.github.io/adk-docs/)
- [Open-Meteo API documentation](https://open-meteo.com/en/docs)
