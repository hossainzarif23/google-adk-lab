# Task Manager — Session State Example

This example applies the session-state concepts from Step 4 of Google's [ADK Agent Team tutorial](https://adk.dev/tutorials/agent-team/) to a task manager. It is a separate learning example, rather than an extension of the tutorial's weather-agent team.

## What it does

The `task_manager` agent uses three tools backed by ADK session state:

- `add_task` adds a task and assigns an incrementing ID.
- `list_tasks` lists all, pending, or completed tasks.
- `complete_task` marks a task as completed.

The tools read and write state through `ToolContext`. `main.py` initializes a session with an empty task list and the next task ID, then sends several requests through the same session to demonstrate state being retained across turns. After each turn, it prints the session state. The agent's `output_key="last_response"` also stores its final response in state.

The example uses `InMemorySessionService`, so session data lasts only while this script is running and is lost when the process exits. It does not provide persistent storage across restarts.

## Requirements

- Python 3.10 or newer
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
- A Xiaomi MiMo API key
- Internet access

## Set up

From the repository root, create and activate the shared virtual environment, then install the dependencies:

### Windows PowerShell

```powershell
uv venv
.venv\Scripts\Activate.ps1
uv pip install google-adk python-dotenv "litellm>=1.84"
```

### macOS or Linux

```bash
uv venv
source .venv/bin/activate
uv pip install google-adk python-dotenv "litellm>=1.84"
```

Create `task-manager/.env` with your API key:

```dotenv
XIAOMI_MIMO_API_KEY="your-xiaomi-mimo-api-key"
```

Keep the key private. The repository-level `.gitignore` excludes `.env` files.

## Run

With the virtual environment activated, run the script from this directory:

### Windows PowerShell

```powershell
Set-Location task-manager
python main.py
```

### macOS or Linux

```bash
cd task-manager
python main.py
```

The script adds two sample tasks, lists them, completes the first task, and lists pending tasks. Edit the `queries` list in `main.py` to try a different sequence.

## Reference

- [ADK Agent Team tutorial — Step 4](https://adk.dev/tutorials/agent-team/)
