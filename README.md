# Google ADK Python Learning Lab

A hands-on learning repository for Google's [Agent Development Kit (ADK) for Python](https://adk.dev/). It includes the Python quickstart, a weather-and-time agent, model comparisons with LiteLLM, and an adapted agent-team example for code review and test design.

## Examples

| Directory | What it demonstrates | How to run |
| --- | --- | --- |
| [`my_agent`](my_agent/) | Quickstart agent that reports the current time for a city | `adk run my_agent` |
| [`multi_tool_agent`](multi_tool_agent/) | Weather and timezone tools in one agent | `adk run multi_tool_agent` |
| [`weather_agent`](weather_agent/) | Agent Team tutorial Steps 1 and 2: weather lookup and Gemini/MiMo comparison | `cd weather_agent` then `python main.py` |
| [`code-review-team`](code-review-team/) | Step 3 delegation pattern adapted to code review and pytest test generation | `cd code-review-team` then `python main.py` |

The `weather_agent` example is still a single agent; later tutorial steps for delegation, session-state personalization, and safety callbacks are not implemented there. `code-review-team` demonstrates delegation with different specialists, but uses code review and test design instead of the tutorial's weather, greeting, and farewell roles. See each directory's README for setup and behavior.

## Requirements and setup

You need Python 3.10 or newer, [`uv`](https://docs.astral.sh/uv/getting-started/installation/), and internet access. The time and weather examples use a Gemini API key. The `weather_agent` model comparison and `code-review-team` use Xiaomi MiMo through LiteLLM.

From the repository root, create a virtual environment and install the dependencies:

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

Create a `.env` file in each agent folder with the credentials that example needs:

- `my_agent/.env` and `multi_tool_agent/.env`: `GOOGLE_API_KEY`
- `weather_agent/.env`: `GOOGLE_API_KEY`, `XIAOMI_MIMO_API_KEY`, and `GOOGLE_GENAI_USE_ENTERPRISE=False`
- `code-review-team/.env`: `XIAOMI_MIMO_API_KEY`

Keep API keys private. The repository `.gitignore` excludes `.env` files, virtual environments, and local ADK session data.

## Run the ADK web interface

With the virtual environment activated, start the development UI from the repository root:

```bash
adk web --port 8000
```

Open <http://localhost:8000> and select `my_agent` or `multi_tool_agent`. The `weather_agent` and `code-review-team` examples use their own Runner scripts as described in their READMEs. ADK Web is for development and debugging, not production use.

## References

- [ADK Python quickstart](https://adk.dev/get-started/python/)
- [ADK Agent Team tutorial](https://adk.dev/tutorials/agent-team/)
- [ADK LiteLLM integration](https://adk.dev/agents/models/litellm/)
- [LiteLLM Xiaomi MiMo provider](https://docs.litellm.ai/docs/providers/xiaomi_mimo)
- [Open-Meteo API documentation](https://open-meteo.com/en/docs)
