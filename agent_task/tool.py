from json_utility import JSONDB
from langchain.tools import tool
from prompt import (
    ADD_TASK_PROMPT,
    EDIT_TASK_PROMPT,
    REMOVE_TASK_PROMPT,
    VIEW_TASK_PROMPT,
)

db = JSONDB()


@tool("add task", description=ADD_TASK_PROMPT)
def add_task(name: str, description: str) -> str:
    """
    Create a new task.

    The task is created with an initial status of 'todo'.

    Args:
        name: Short title of the task.
        description: Detailed description of the task.

    Returns:
        A message indicating whether the task was created or updated.
    """
    result = db.save_task(
        name=name,
        description=description,
        status="todo",
    )
    return result


@tool("remove task", description=REMOVE_TASK_PROMPT)
def remove_task(name: str) -> str:
    """
    Delete an existing task.

    Args:
        name: Name of the task to delete.

    Returns:
        Success or failure message.
    """
    result = db.delete_task(name=name)

    if result:
        return f"Successfully deleted task '{name}'."

    return f"Unable to find task '{name}'."


@tool("edit task status", description=EDIT_TASK_PROMPT)
def edit_task_status(name: str, status: str) -> str:
    """
    Update the status of an existing task.

    Expected status values:
    - todo
    - in_progress
    - completed

    Args:
        name: Name of the task to update.
        status: New status for the task.

    Returns:
        Success or failure message.
    """
    result = db.update_task_status(
        name=name,
        new_status=status,
    )

    if result:
        return f"Updated task '{name}' status to '{status}'."

    return f"Unable to find task '{name}'."


@tool("view tasks", description=VIEW_TASK_PROMPT)
def view_tasks() -> str:
    """
    Retrieve all stored tasks.

    Returns:
        A formatted string containing all tasks or a message
        indicating that no tasks exist.
    """
    result = db.fetch_all_tasks()

    if result:
        return f"All tasks: {result}"

    return "No tasks exist. Start by adding one."
