import json

from mcp.server.fastmcp import FastMCP
from prompt import RAG_PROMPT

mcp = FastMCP("WeatherServer")


@mcp.tool(description=RAG_PROMPT)
def rag_tool(query: str) -> str:
    """
    Retrieve information from the knowledge base.

    Args:
        query: Question or search query.

    Returns:
        Relevant knowledge base entries.
    """

    print("rag tool invoked")

    with open("sample_data.json") as f:
        docs = json.load(f)

    results = []

    for word in query.split():
        for doc in docs:
            text = f"{doc['title']} {doc['content']}"

            if word.lower() in text.lower():
                results.append(doc["content"])

    if not results:
        return "No relevant documents found."

    return "\n".join(results)


if __name__ == "__main__":
    mcp.run()
