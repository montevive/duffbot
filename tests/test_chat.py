import pytest
import asyncio
from backend.routers.chat import web_search_brave

@pytest.mark.asyncio
async def test_concurrent_web_search_brave():
    # Create multiple concurrent search tasks
    search_tasks = [
        web_search_brave("python programming"),
        web_search_brave("artificial intelligence"),
        web_search_brave("web development"),
        web_search_brave("data science"),
        web_search_brave("machine learning"),
    ]

    # Run the tasks concurrently
    results = await asyncio.gather(*search_tasks)

    # Check that we got the expected number of results
    assert len(results) == 5

    for result in results:
        # Check that each result is a string (as returned by the function)
        assert isinstance(result, str)
        
        # Check that each result contains the expected structure
        assert result.startswith("[{") and result.endswith("}]")
        
        # Check that each result contains at least one search result
        assert "title" in result and "description" in result and "url" in result

    # Check if any result indicates a rate limit error
    rate_limit_errors = [result for result in results if "Rate limit exceeded" in result]
    
    if rate_limit_errors:
        print(f"Number of rate limit errors: {len(rate_limit_errors)}")
        print("Rate limiting observed, retry mechanism activated.")
    else:
        print("No rate limiting observed in this test run.")
