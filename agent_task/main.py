import asyncio
from os import getenv

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from prompt import SYSTEM_PROMPT
from tool import add_task, edit_task_status, remove_task, view_tasks

load_dotenv()

OPENAI_API_KEY = getenv("OPENAI_API_KEY", None)
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not present in .env")


async def main():
    client = MultiServerMCPClient(
        {
            "rag": {
                "command": "python",
                "args": ["rag_mcp.py"],
                "transport": "stdio",
            }
        }
    )

    mcp_tools = await client.get_tools()
    agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[add_task, remove_task, edit_task_status, view_tasks, *mcp_tools],
    )

    message = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
        ]
    }
    user_query = input("Enter Query: ")

    message["messages"].append({"role": "user", "content": user_query})

    result = await agent.ainvoke(message)
    # print(f"RESULT: {result}")
    print("AI Response: ", result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
