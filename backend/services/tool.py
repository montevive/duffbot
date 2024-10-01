import aiohttp
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed
import json
import redis.asyncio as redis
from config.settings import BRAVE_SEARCH_API_KEY, REDIS

redis_client = redis.from_url(REDIS, encoding="utf-8", decode_responses=True)

async def web_search_brave(query: str) -> str:
    @retry(
        stop=stop_after_attempt(15),
        wait=wait_fixed(1),
        retry=retry_if_exception_type(aiohttp.ClientResponseError)
    )
    async def _perform_search():
        url = "https://api.search.brave.com/res/v1/web/search"
        
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": BRAVE_SEARCH_API_KEY
        }
        
        params = {
            "q": query,
            "count": 3
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    results = await response.json()
                    web_results = results.get('web', {}).get('results', [])
                    formatted_results = [
                        {
                            "title": result.get('title'),
                            "description": result.get('description'),
                            "url": result.get('url')
                        }
                        for result in web_results[:3]
                    ]
                    return str(formatted_results)
                elif response.status == 429:  # Too Many Requests
                    raise aiohttp.ClientResponseError(
                        response.request_info,
                        response.history,
                        status=response.status,
                        message="Rate limit exceeded"
                    )
                else:
                    return f"Error performing Brave search: {response.status}"

    try:
        return await _perform_search()
    except aiohttp.ClientResponseError as e:
        return f"Error performing Brave search after retries: {e}"

async def register_tool(tool_name: str, reason: str, description: str, website: str = None) -> str:
    tool_data = {
        'tool_name': tool_name,
        'description': description,
        'website': website
    }
    tool_json = json.dumps(tool_data)
    
    # Store the tool information in a Redis list
    await redis_client.rpush('duffbot_tools', tool_json)
    
    # Store the tool data for retrieval by tool_name
    await redis_client.hset('duffbot_tool_data', tool_name, tool_json)
    
    # Update the count of tool occurrences
    await redis_client.zincrby('duffbot_tool_ranking', 1, tool_name)
    
    # Add the reason to the list of reasons for this tool
    await redis_client.rpush(f'duffbot_tool_reasons:{tool_name}', reason)
    return f"Registered AI tool: {tool_name}. Reason: {reason}. Website: {website}"

