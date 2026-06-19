from langchain.tools import tool
from prompt import (
    ADD_TASK_PROMPT,
    EDIT_TASK_PROMPT,
    REMOVE_TASK_PROMPT,
    VIEW_TASK_PROMPT,
)

from agent_task.json_utility import JSONDB

db = JSONDB()


@tool("add task", description=ADD_TASK_PROMPT)
def add_task(name: str, description: str) -> str:
    result = db.save_task(name=name, description=description, status="todo")
    return result


@tool("remove task", description=REMOVE_TASK_PROMPT)
def remove_task(name: str) -> str:
    result = db.delete_task(name=name)
    if result:
        return f"successfully deleted {name} task"
    else:
        return f"unable to find {name} task"


@tool("edit task status", description=EDIT_TASK_PROMPT)
def edit_task_status(name: str, status: str) -> str:
    result = db.update_task_status(name=name, new_status=status)
    if result:
        return f"Updated {name} status to {status}"
    else:
        return f"Unable to find {name} task"


@tool("view tasks", description=VIEW_TASK_PROMPT)
def view_tasks() -> str:
    result = db.fetch_all_tasks()
    if result:
        return f"all tasks: {result}"
    else:
        return "no tasks exist, start by adding one"
