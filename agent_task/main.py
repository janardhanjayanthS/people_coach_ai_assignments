from os import getenv
from uuid import uuid4

from dotenv import load_dotenv
from langchain.agents import create_agent
from prompt import SYSTEM_PROMPT

load_dotenv()

OPENAI_API_KEY = getenv("OPENAI_API_KEY", None)
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not present in .env")

agent = create_agent(model="openai:gpt-4o-mini")

config = {"configurable": {"thread_id": str(uuid4())}}

message = {
    "messages": [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]
}


while True:
    user_query = input("Enter Query: ")

    if user_query.lower() in {"exit", "quit", "q", "e"}:
        break

    message["messages"].append({"role": "user", "content": user_query})

    result = agent.invoke(
        message,
        config=config,
    )
    print(result)
