from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google.adk.models.lite_llm import LiteLlm


load_dotenv()  # Load environment variables from .env file


def add_task(title: str, tool_context: ToolContext) -> dict:
    """Add a new task to the user's task list.

    Args:
        title: A short description of the task.
    """
    title = title.strip()

    if not title:
        return {
            "status": "error",
            "message": "Task title cannot be empty.",
        }

    tasks = list(tool_context.state.get("tasks", []))
    task_id = tool_context.state.get("next_task_id", 1)

    task = {
        "id": task_id,
        "title": title,
        "completed": False,
    }

    tasks.append(task)

    tool_context.state["tasks"] = tasks
    tool_context.state["next_task_id"] = task_id + 1

    return {
        "status": "success",
        "task": task,
    }


def list_tasks(status: str, tool_context: ToolContext) -> dict:
    """List tasks, optionally filtering by their completion status.

    Args:
        status: One of 'all', 'pending', or 'completed'.
    """
    if status not in ("all", "pending", "completed"):
        return {
            "status": "error",
            "message": "Status must be all, pending, or completed.",
        }

    tasks = tool_context.state.get("tasks", [])

    if status == "pending":
        tasks = [task for task in tasks if not task["completed"]]
    elif status == "completed":
        tasks = [task for task in tasks if task["completed"]]

    return {
        "status": "success",
        "tasks": tasks,
        "count": len(tasks),
    }


def complete_task(
    task_id: int,
    tool_context: ToolContext,
) -> dict:
    """Mark an existing task as completed.

    Args:
        task_id: The numeric ID of the task to complete.
    """
    tasks = [task.copy() for task in tool_context.state.get("tasks", [])]

    for task in tasks:
        if task["id"] == task_id:
            if task["completed"]:
                return {
                    "status": "success",
                    "message": "Task is already completed.",
                    "task": task,
                }

            task["completed"] = True
            tool_context.state["tasks"] = tasks

            return {
                "status": "success",
                "message": "Task completed.",
                "task": task,
            }

    return {
        "status": "error",
        "message": f"Task #{task_id} not found.",
    }


root_agent = Agent(
    name="task_manager",
    model=LiteLlm(model="xiaomi_mimo/mimo-v2.6-flash"),
    description=("An assistant that manages tasks using session state."),
    instruction=(
        "You are a helpful task management assistant. Use add_task to create tasks, list_tasks to retrieve tasks, "
        "and complete_task to mark tasks as completed. Always use these tools for task operations. "
        "Do not invent task IDs, tasks, or completion statuses. When listing tasks, pass the appropriate status: "
        "'all', 'pending', or 'completed'. When the user refers to a task ambiguously, use list_tasks "
        "to identify it, and ask for clarification if necessary. After a tool operation, briefly summarize the result. "
        "If a tool returns an error, explain it clearly."
    ),
    tools=[add_task, list_tasks, complete_task],
    output_key="last_response",
)
