from os import getenv

from dotenv import load_dotenv
from langchain.agents import create_agent
from prompt import SYSTEM_PROMPT
from tool import add_task, edit_task_status, remove_task, view_tasks

load_dotenv()

OPENAI_API_KEY = getenv("OPENAI_API_KEY", None)
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not present in .env")

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[add_task, remove_task, edit_task_status, view_tasks],
)


message = {
    "messages": [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]
}


if __name__ == "__main__":
    user_query = input("Enter Query: ")

    message["messages"].append({"role": "user", "content": user_query})

    result = agent.invoke(message)
    print("AI Response: ", result["messages"][2].content)
