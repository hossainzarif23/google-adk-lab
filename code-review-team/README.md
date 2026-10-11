# Code Review Team

A small multi-agent example inspired by Step 3 of Google's [ADK Agent Team tutorial](https://adk.dev/tutorials/agent-team/). A coordinator delegates Python code-review requests and test-generation requests to separate specialist agents. This adapts the tutorial's delegation pattern; the tutorial's sample specialists handle weather, greetings, and farewells.

## Agents and flow

- `code_review_coordinator` routes requests about bugs and correctness to `code_reviewer`, and requests for pytest tests to `test_designer`.
- Both specialists use Xiaomi MiMo through ADK's LiteLLM integration.
- `main.py` loads `sample_code.py`, creates an in-memory ADK session for each request, then sends one review request and one test-generation request through the coordinator. It prints agent handoffs, tool events, and final responses.
- `sample_code.py` contains a `find_max` example with a bug for the reviewer to identify: initializing the maximum to zero gives the wrong answer for a list containing only negative numbers.

The test designer generates test code and explains assumptions. The app does not execute the generated tests; its instruction explicitly tells the specialist not to claim that it did.

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

Create `code-review-team/.env` with your MiMo API key:

```dotenv
XIAOMI_MIMO_API_KEY="your-xiaomi-mimo-api-key"
```

Keep the key private. The repository-level `.gitignore` excludes `.env` files.

## Run

With the virtual environment activated, run the script from this directory:

### Windows PowerShell

```powershell
Set-Location code-review-team
python main.py
```

### macOS or Linux

```bash
cd code-review-team
python main.py
```

You should see the coordinator delegate the first request to `code_reviewer` and the second to `test_designer`. The test code appears in the output for review; it is not run by this script. To use different input, edit `sample_code.py` or the queries in `main.py`.

## References

- [ADK Agent Team tutorial](https://adk.dev/tutorials/agent-team/)
- [ADK LiteLLM integration](https://adk.dev/agents/models/litellm/)
- [LiteLLM Xiaomi MiMo provider](https://docs.litellm.ai/docs/providers/xiaomi_mimo)
