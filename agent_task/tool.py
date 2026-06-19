from langchain.tools import tool
from prompt import (
    ADD_TASK_PROMPT,
    EDIT_TASK_PROMPT,
    REMOVE_TASK_PROMPT,
    VIEW_TASK_PROMPT,
)


@tool("add task", description=ADD_TASK_PROMPT)
def add_task(name: str, description: str) -> None:
    pass


@tool("remove task", description=REMOVE_TASK_PROMPT)
def remove_task(name: str) -> None:
    pass


@tool("edit task status", description=EDIT_TASK_PROMPT)
def edit_task_status(name: str, status: str) -> None:
    pass


@tool("view tasks", description=VIEW_TASK_PROMPT)
def view_taskas() -> str:
    return ""
