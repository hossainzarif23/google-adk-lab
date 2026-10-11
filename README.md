# Google ADK Python Learning Lab

A hands-on learning repository for Google's [Agent Development Kit (ADK) for Python](https://adk.dev/). It contains a quickstart agent, an expanded weather-and-time example, and work through Step 2 of the [ADK Agent Team tutorial](https://adk.dev/tutorials/agent-team/).

## Examples

| Directory | What it demonstrates | How to run |
| --- | --- | --- |
| [`my_agent`](my_agent/) | Quickstart agent that reports the current time for a city | `adk run my_agent` |
| [`multi_tool_agent`](multi_tool_agent/) | Weather and timezone tools in one agent | `adk run multi_tool_agent` |
| [`weather_agent`](weather_agent/) | Tutorial Steps 1 and 2: a weather agent, an Open-Meteo tool, and a Gemini/MiMo comparison through LiteLLM | `cd weather_agent` then `python main.py` |

The `weather_agent` directory implements the single-agent weather lookup and optional multi-model comparison. Later tutorial steps—agent delegation, session-state personalization, and safety callbacks—are not implemented yet. See its [README](weather_agent/README.md) for setup and run instructions.

## Shared setup

Requirements: Python 3.10 or newer, [`uv`](https://docs.astral.sh/uv/getting-started/installation/), a Gemini API key, and an internet connection. The `weather_agent` comparison also needs a Xiaomi MiMo API key.

From the repository root, create a virtual environment and install the dependencies used by the examples:

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

For `my_agent` and `multi_tool_agent`, save your Gemini key in the selected agent folder's `.env` file:

```dotenv
GOOGLE_API_KEY="your-api-key"
```

For `weather_agent`, set both `GOOGLE_API_KEY` and `XIAOMI_MIMO_API_KEY` in `weather_agent/.env`, and set `GOOGLE_GENAI_USE_ENTERPRISE=False` to use the Gemini API key. See its [README](weather_agent/README.md) for details. Local `.env` files, virtual environments, and ADK session data are ignored by Git.

## Run the ADK web interface

With the virtual environment activated, start the development UI from the repository root:

```bash
adk web --port 8000
```

Open <http://localhost:8000> and select `my_agent` or `multi_tool_agent`. The tutorial's `weather_agent` example uses its own Runner script described in its README. ADK Web is for development and debugging, not production use.

## References

- [ADK Python quickstart](https://adk.dev/get-started/python/)
- [ADK Agent Team tutorial](https://adk.dev/tutorials/agent-team/)
- [Open-Meteo API documentation](https://open-meteo.com/en/docs)
