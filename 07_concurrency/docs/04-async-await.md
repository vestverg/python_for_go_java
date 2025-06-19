# Async/Await in Python

## 🎯 Overview

AsyncIO enables writing concurrent code using async/await syntax. Perfect for I/O-bound tasks with high concurrency requirements.

## 🚀 Basic AsyncIO

### Coroutines and Event Loop

```python
import asyncio
import time

async def hello_async():
    print("Hello")
    await asyncio.sleep(1)  # Non-blocking sleep
    print("World")

# Running async code
asyncio.run(hello_async())

# Multiple coroutines
async def say_after(delay, message):
    await asyncio.sleep(delay)
    print(message)

async def concurrent_example():
    # Sequential (3 seconds)
    await say_after(1, "Hello")
    await say_after(2, "World")
    
    # Concurrent (2 seconds)
    task1 = asyncio.create_task(say_after(1, "Hello"))
    task2 = asyncio.create_task(say_after(2, "World"))
    await task1
    await task2

asyncio.run(concurrent_example())
```

### Task Management

```python
import asyncio

async def worker(name, work_time):
    print(f"{name} started")
    await asyncio.sleep(work_time)
    print(f"{name} completed")
    return f"Result from {name}"

async def task_management():
    # Method 1: gather - run concurrently
    results = await asyncio.gather(
        worker("Worker-A", 1),
        worker("Worker-B", 2),
        worker("Worker-C", 1.5)
    )
    print(f"Results: {results}")

asyncio.run(task_management())
```

## 🌐 HTTP Requests with AsyncIO

```python
import asyncio
import aiohttp
import time

async def fetch_url(session, url):
    try:
        async with session.get(url) as response:
            data = await response.json()
            return {"url": url, "status": response.status, "success": True}
    except Exception as e:
        return {"url": url, "error": str(e), "success": False}

async def fetch_multiple_urls():
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3",
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    
    for result in results:
        if result["success"]:
            print(f"✓ {result['url']}: {result['status']}")
        else:
            print(f"✗ {result['url']}: {result['error']}")

asyncio.run(fetch_multiple_urls())
```

## 🔄 Async Patterns

### Producer-Consumer

```python
import asyncio
import random

async def producer(queue, name, count):
    for i in range(count):
        item = f"{name}-Item-{i}"
        await queue.put(item)
        print(f"Produced: {item}")
        await asyncio.sleep(0.1)

async def consumer(queue, name):
    while True:
        try:
            item = await asyncio.wait_for(queue.get(), timeout=2.0)
            print(f"{name} consumed: {item}")
            queue.task_done()
        except asyncio.TimeoutError:
            break

async def producer_consumer_example():
    queue = asyncio.Queue(maxsize=5)
    
    # Start producer and consumers
    await asyncio.gather(
        producer(queue, "Producer", 10),
        consumer(queue, "Consumer-1"),
        consumer(queue, "Consumer-2"),
    )

asyncio.run(producer_consumer_example())
```

## ⏱️ Timeouts and Error Handling

```python
import asyncio
import aiohttp

async def fetch_with_timeout(url, timeout=5):
    try:
        async with aiohttp.ClientSession() as session:
            async with asyncio.timeout(timeout):  # Python 3.11+
                async with session.get(url) as response:
                    return await response.text()
    except asyncio.TimeoutError:
        return f"Timeout after {timeout} seconds"
    except Exception as e:
        return f"Error: {e}"

async def error_handling_example():
    tasks = [
        fetch_with_timeout("https://httpbin.org/delay/1", 5),
        fetch_with_timeout("https://httpbin.org/delay/10", 3),  # Will timeout
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Task {i} failed: {result}")
        else:
            print(f"Task {i} success: {len(result)} bytes")

asyncio.run(error_handling_example())
```

## 🎯 When to Use AsyncIO

### ✅ Perfect Use Cases
- **High-volume HTTP requests**
- **WebSocket connections**
- **Database I/O with async drivers**
- **Real-time applications**
- **API gateways**

### ⚠️ Consider Alternatives
- **CPU-bound tasks** (use multiprocessing)
- **Simple I/O operations** (threading might be simpler)
- **Legacy codebases** (integration complexity)

## 🔗 Next Steps

- **Performance optimization**: [Performance Guide →](05-performance.md)
- **Production patterns**: [Production Patterns →](07-production-patterns.md) 