# Weather Agent — ADK Tutorial Steps 1 and 2

This project follows the first two parts of Google's [ADK Agent Team tutorial](https://adk.dev/tutorials/agent-team/): a single weather agent with an Open-Meteo tool, then an optional multi-model comparison using Gemini and Xiaomi MiMo through LiteLLM.

The later tutorial steps—delegation to a team of agents, session-state personalization, and safety callbacks—have not been implemented yet.

## What it does

- [`agent.py`](agent.py) defines the weather lookup tool and builds the agent for either Gemini or MiMo.
- The `get_weather` tool resolves a city with the Open-Meteo Geocoding API and retrieves current weather from the Forecast API. It returns temperature, relative humidity, apparent temperature, precipitation, weather code, wind speed, and their units.
- [`main.py`](main.py) creates an in-memory session and ADK `Runner` for each provider, then sends the same comparison question to MiMo and Gemini in sequence. It prints tool calls, tool results, and final responses.

The script compares New York, Paris, and Tokyo. Geocoding uses the first result, so include a country when a city name could be ambiguous. Open-Meteo needs internet access but no API key; both model providers need their own API key to run the full comparison.

## Requirements

- Python 3.10 or newer
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)
- A Xiaomi MiMo API key
- Internet access for the model providers and Open-Meteo

## Set up

From the repository root, create and activate the shared virtual environment, then install the dependencies:

### Windows PowerShell

```powershell
uv venv
.venv\Scripts\Activate.ps1
uv pip install google-adk requests python-dotenv "litellm>=1.84"
```

### macOS or Linux

```bash
uv venv
source .venv/bin/activate
uv pip install google-adk requests python-dotenv "litellm>=1.84"
```

Create `weather_agent/.env` with your provider settings:

```dotenv
GOOGLE_GENAI_USE_ENTERPRISE=False
GOOGLE_API_KEY="your-google-api-key"
XIAOMI_MIMO_API_KEY="your-xiaomi-mimo-api-key"
```

Keep these keys private. The repository-level `.gitignore` excludes `.env` files.

## Run the comparison

With the virtual environment activated, run the script from this directory. Its imports expect the current working directory to be `weather_agent`.

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

The script sends a fixed sample question to each provider; it is not an interactive chat loop. Change the query in `main.py` to compare another request.

## References

- [ADK Agent Team tutorial](https://adk.dev/tutorials/agent-team/)
- [ADK LiteLLM integration](https://google.github.io/adk-docs/agents/models/litellm/)
- [LiteLLM Xiaomi MiMo provider](https://docs.litellm.ai/docs/providers/xiaomi_mimo)
- [Open-Meteo API documentation](https://open-meteo.com/en/docs)
