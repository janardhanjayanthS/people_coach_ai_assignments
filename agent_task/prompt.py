SYSTEM_PROMPT = """
You are a helpful assistant!

RULES:
- Respond appropriately for the user query
- Use tools based on user query
- Whenever passing any arguments to any tools
    all string must be lowercase
"""

ADD_TASK_PROMPT = """
Create a new task in the task manager.
If you get no description generate a small
from the prompt

Use this tool when the user wants to:
- add a task
- create a task
- remember something for later
- add an item to a todo list

Arguments:
- name: short title of the task
- description: details about the task

New tasks are automatically created with status 'todo'.
"""

VIEW_TASK_PROMPT = """
Retrieve and display all tasks currently stored.

Use this tool when the user wants to:
- view tasks
- list tasks
- show tasks
- see todo items
- check task status

No arguments required.
"""

REMOVE_TASK_PROMPT = """
Delete an existing task.

Use this tool when the user wants to:
- remove a task
- delete a task
- mark a task as no longer needed

Arguments:
- name: exact task name to remove
"""

EDIT_TASK_PROMPT = """
Update the status of an existing task.

Use this tool when the user wants to:
- mark a task as completed
- change task status
- move a task to in_progress
- reopen a task

Arguments:
- name: task name
- status: one of
  - todo
  - in_progress
  - completed
"""
