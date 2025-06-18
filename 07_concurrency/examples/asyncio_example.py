#!/usr/bin/env python3

"""
Example demonstrating Python's asyncio capabilities.
"""

import asyncio
import aiohttp
import time
from typing import List, Dict, Any
from dataclasses import dataclass
import random


@dataclass
class ApiResult:
    """Represents an API call result"""
    url: str
    status: int
    data: Dict[str, Any]
    elapsed: float


async def fetch_url(session: aiohttp.ClientSession, url: str) -> ApiResult:
    """
    Fetch data from a URL asynchronously.
    
    Args:
        session: aiohttp session
        url: URL to fetch
    
    Returns:
        ApiResult containing response data
    """
    start_time = time.time()
    
    try:
        async with session.get(url) as response:
            data = await response.json()
            elapsed = time.time() - start_time
            return ApiResult(url, response.status, data, elapsed)
    except Exception as e:
        elapsed = time.time() - start_time
        return ApiResult(url, 500, {"error": str(e)}, elapsed)


async def process_api_result(result: ApiResult) -> None:
    """
    Process API result asynchronously.
    
    Args:
        result: API result to process
    """
    # Simulate some processing
    await asyncio.sleep(random.uniform(0.1, 0.3))
    
    print(f"\nProcessed result from {result.url}")
    print(f"Status: {result.status}")
    print(f"Time: {result.elapsed:.2f} seconds")
    print(f"Data: {result.data}")


async def fetch_all_urls(urls: List[str]) -> List[ApiResult]:
    """
    Fetch multiple URLs concurrently.
    
    Args:
        urls: List of URLs to fetch
    
    Returns:
        List of API results
    """
    async with aiohttp.ClientSession() as session:
        # Create tasks for all URLs
        tasks = [
            fetch_url(session, url)
            for url in urls
        ]
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)
        return results


async def main():
    # Example URLs (JSONPlaceholder API)
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3",
        "https://jsonplaceholder.typicode.com/posts/4",
        "https://jsonplaceholder.typicode.com/posts/5"
    ]
    
    print("Fetching URLs...")
    start_time = time.time()
    
    # Fetch all URLs
    results = await fetch_all_urls(urls)
    
    print(f"\nFetched {len(results)} URLs in {time.time() - start_time:.2f} seconds")
    
    # Process results concurrently
    print("\nProcessing results...")
    process_tasks = [
        process_api_result(result)
        for result in results
    ]
    
    await asyncio.gather(*process_tasks)


async def periodic_task(interval: float) -> None:
    """
    Example of a periodic task using asyncio.
    
    Args:
        interval: Time between executions in seconds
    """
    while True:
        print(f"\nPeriodic task executed at {time.strftime('%H:%M:%S')}")
        await asyncio.sleep(interval)


async def run_with_timeout():
    """Run main tasks with a timeout and a background task"""
    # Create background task
    background_task = asyncio.create_task(periodic_task(2.0))
    
    try:
        # Run main function with timeout
        await asyncio.wait_for(main(), timeout=10.0)
    except asyncio.TimeoutError:
        print("\nTimeout occurred!")
    finally:
        # Cancel background task
        background_task.cancel()
        try:
            await background_task
        except asyncio.CancelledError:
            print("\nBackground task cancelled")


if __name__ == "__main__":
    # Run event loop
    asyncio.run(run_with_timeout()) 