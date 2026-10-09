# Google ADK Python Quickstart

A small learning project built from the [Agent Development Kit (ADK) Python quickstart](https://adk.dev/get-started/python/). It defines a Gemini-powered assistant that looks up the current time for a requested IANA timezone using a Python tool.

## What’s in this repository

- `my_agent/agent.py` defines `root_agent` and its `get_current_time` tool.
- `my_agent/__init__.py` exposes the agent package for ADK.
- `my_agent/.env` holds your local Gemini API key. This file is ignored by Git.

The tool accepts timezone names such as `Asia/Dhaka` or `Europe/London` and returns the current time in ISO 8601 format. If the timezone name is invalid, it returns an error instead of making up a time.

## Requirements

- Python 3.10 or newer
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

## Set up

Run these commands from the repository root.

### Windows PowerShell

```powershell
uv venv
.venv\Scripts\Activate.ps1
uv pip install google-adk
```

### macOS or Linux

```bash
uv venv
source .venv/bin/activate
uv pip install google-adk
```

Create `my_agent/.env` and add your API key:

```dotenv
GOOGLE_API_KEY="your-api-key"
```

Keep this key private. The `.env` file is excluded from version control.

## Run the agent

With the virtual environment activated, run the interactive command-line version from the repository root:

```bash
adk run my_agent
```

Or start ADK’s local development chat interface:

```bash
adk web --port 8000
```

Open <http://localhost:8000> and select `my_agent`. ADK Web is intended for development and debugging, not production use.

Try asking: “What time is it in Dhaka?” The assistant should determine the city’s timezone and use the tool to get the current time.

## Learn more

- [ADK Python quickstart](https://adk.dev/get-started/python/)
- [ADK documentation](https://google.github.io/adk-docs/)
