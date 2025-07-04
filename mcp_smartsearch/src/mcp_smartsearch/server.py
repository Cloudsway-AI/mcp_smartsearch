import os
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("SmartSearchService")

@mcp.tool()
async def smart_search(
    query: str,
    count: int = 10,
    offset: int = 0,
    setLang: str = 'en',
    safeSearch: str = 'Strict'
) -> dict:
    """
    Performs a web search using a remote smart search API.
    Returns a JSON object with the search results.
    """
    server_key = os.getenv("SERVER_KEY")
    if not server_key:
        raise ValueError("SERVER_KEY environment variable is not set.")

    try:
        endpoint, api_key = server_key.split("-", 1)
    except ValueError:
        raise ValueError("Invalid SERVER_KEY format. Expected 'endpoint-apikey'.")

    url = f"https://searchapi.xiaosuai.com/search/{endpoint}/smart"
    params = {
        'q': query,
        'count': count,
        'offset': offset,
        'mkt': setLang,
        'safeSearch': safeSearch
    }
    headers = {'Authorization': f'Bearer {api_key}'}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio")
