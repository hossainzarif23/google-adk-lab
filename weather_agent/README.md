# Weather Agent — ADK Tutorial Step 1

This directory contains the first step of Google's [ADK Agent Team tutorial](https://adk.dev/tutorials/agent-team/): a single weather agent with one tool that retrieves current conditions for a city. The later agent-team, state, and guardrail steps have not been implemented here yet.

## How it works

- [`agent.py`](agent.py) defines `root_agent` and its `get_weather` tool.
- The tool resolves a city using the [Open-Meteo Geocoding API](https://open-meteo.com/en/docs/geocoding-api), then requests current weather from the [Open-Meteo Forecast API](https://open-meteo.com/en/docs).
- The returned conditions include temperature, relative humidity, apparent temperature, precipitation, weather code, and wind speed.
- [`main.py`](main.py) creates an in-memory session and an ADK `Runner`, then sends two sample questions (New York and Paris) in the same session and prints the run events and responses.

The geocoding request uses its first result. If a city name is ambiguous, include a country in the query. Open-Meteo requires an internet connection but this example does not need an Open-Meteo API key. Gemini does require a Google API key.

## Requirements

- Python 3.10 or newer
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)
- Internet access for Gemini and Open-Meteo

## Set up

From the repository root, create and activate the shared virtual environment, then install the dependencies:

### Windows PowerShell

```powershell
uv venv
.venv\Scripts\Activate.ps1
uv pip install google-adk requests python-dotenv
```

### macOS or Linux

```bash
uv venv
source .venv/bin/activate
uv pip install google-adk requests python-dotenv
```

Create `weather_agent/.env` with your Gemini API key:

```dotenv
GOOGLE_API_KEY="your-api-key"
```

Keep the key private. The repository-level `.gitignore` excludes `.env` files.

## Run

The script imports `agent` from the current directory, so run it from `weather_agent` with the virtual environment activated:

### Windows PowerShell

```powershell
Set-Location weather_agent
python main.py
```

### macOS or Linux

```bash
cd weather_agent
python main.py
```

The script currently sends its two sample queries automatically; it is not an interactive chat loop. To try a different query, edit the `call_agent_async(...)` calls in `main.py`.

## Tutorial reference

- [ADK Agent Team tutorial](https://adk.dev/tutorials/agent-team/)
