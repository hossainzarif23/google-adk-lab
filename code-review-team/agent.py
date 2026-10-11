from google.adk.agents import Agent
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm


load_dotenv()  # Load environment variables from .env file


code_reviewer = Agent(
    name="code_reviewer",
    model=LiteLlm(model="xiaomi_mimo/mimo-v2.6-flash"),
    description="Reviews Python code for bugs, logical errors, edge cases, and correctness issues.",
    instruction=(
        "You are an experienced Python code reviewer. Review the Python code provided by the user. "
        "Focus on correctness, logical bugs, and edge cases. Explain each issue clearly and suggest minimal fixes. "
        "Do not invent issues or rewrite working code unnecessarily. If the code looks correct, say so. Do not execute the code."
    ),
)


test_designer = Agent(
    name="test_designer",
    model=LiteLlm(model="xiaomi_mimo/mimo-v2.6-flash"),
    description="Generates pytest unit tests and test cases for Python functions.",
    instruction=(
        "You are a Python testing specialist. Generate pytest tests for the code provided by the user. "
        "Cover normal behavior, edge cases, and likely failure cases. Make reasonable assumptions when behavior is unclear, "
        "and state those assumptions. Provide runnable test code when enough context is available. "
        "Do not claim that tests were executed."
    ),
)


root_agent = Agent(
    name="code_review_coordinator",
    model=LiteLlm(model="xiaomi_mimo/mimo-v2.6-flash"),
    description="Coordinates specialized agents for Python "
    "code review and test generation.",
    instruction=(
        "You are the coordinator of a Python code review team. Your job is to delegate requests to the appropriate specialist. "
        "If the user asks to review code, identify bugs, explain errors, or suggest fixes, "
        "delegate to code_reviewer. If the user asks to generate unit tests, pytest tests, "
        "or test cases, delegate to test_designer. Do not perform specialized reviews or write tests yourself. "
        "Let the appropriate specialist handle the request. If the user's request is unclear, ask for clarification. "
        "If the request needs both specialists, explain that you can handle the review and testing as separate tasks."
    ),
    sub_agents=[code_reviewer, test_designer],
)
