# ⚡ Concurrency - Knowledge Check

> **Unlock parallel Python power!** 🚀  
> Master threading, multiprocessing, and async/await patterns.

---

## 📊 **Progress Tracker**
**Section:** Concurrency | **Questions:** 6 | **Difficulty:** Advanced | **Time:** ~8 min

---

### 🎯 **Question 1 of 6**
**Which module handles multithreading in Python?**

```python
# Concurrency options in Python:
import threading    # For I/O-bound tasks
import multiprocessing  # For CPU-bound tasks  
import asyncio     # For async/await patterns
```

**A.** `multiprocessing`  
**B.** `threading`  
**C.** `asyncio`  

---

### 🎯 **Question 2 of 6**
**How do you define an async function?**

```python
# Synchronous function:
def fetch_data():
    return requests.get('https://api.example.com')

# Asynchronous function:
??? def fetch_data():
    return await aiohttp.get('https://api.example.com')
```

**A.** `async def fetch_data():`  
**B.** `await def fetch_data():`  
**C.** `future def fetch_data():`  

---

### 🎯 **Question 3 of 6**
**What is the GIL in Python?**

```python
# The Global Interpreter Lock affects:
import threading

def cpu_bound_task():
    # Heavy computation
    result = sum(i*i for i in range(1000000))
    return result

# Multiple threads won't speed this up because of...?
```

**A.** Global Interpreter Lock  
**B.** General Import Library  
**C.** Global Instance Loader  

---

### 🎯 **Question 4 of 6**
**When should you use multiprocessing vs threading?**

```python
# CPU-bound: Heavy computation
def calculate_primes(n):
    # Complex math operations
    pass

# I/O-bound: Network requests, file operations  
def download_files(urls):
    # Waiting for network/disk
    pass
```

**A.** Threading for CPU, multiprocessing for I/O  
**B.** Multiprocessing for CPU, threading for I/O  
**C.** Always use threading  

---

### 🎯 **Question 5 of 6**
**What does `await` do in an async function?**

```python
async def main():
    print("Starting...")
    result = await slow_network_call()  # What happens here?
    print(f"Got: {result}")
    
# The function pauses execution until...?
```

**A.** The awaited result is ready  
**B.** A new thread starts  
**C.** The function completes  

---

### 🎯 **Question 6 of 6**
**How do you run multiple async tasks concurrently?**

```python
import asyncio

async def task1(): 
    await asyncio.sleep(1)
    return "Task 1"

async def task2():
    await asyncio.sleep(1) 
    return "Task 2"

# Run both tasks concurrently:
results = await ???([task1(), task2()])
```

**A.** `asyncio.run()`  
**B.** `asyncio.gather()`  
**C.** `asyncio.wait()`

---

## 🎉 **Concurrency Master!**

### ⚡ **Python Concurrency Models:**
- **Threading** → I/O-bound tasks, GIL limitation
- **Multiprocessing** → CPU-bound tasks, true parallelism
- **Asyncio** → High-concurrency I/O, single-threaded
- **Concurrent.futures** → High-level interface

### 🔄 **Language Comparison:**
| Feature | Java | Go | Python |
|---------|------|----|---------| 
| **Threads** | Native threads | Goroutines | GIL-limited |
| **Async/await** | CompletableFuture | Built-in | asyncio |
| **Process pools** | ForkJoinPool | ❌ | multiprocessing |
| **Memory sharing** | Synchronized | Channels | Queues/Pipes |

### 🎯 **Best Practices:**
- **CPU-bound** → Use `multiprocessing`
- **I/O-bound** → Use `asyncio` or `threading`  
- **Mixed workloads** → Combine approaches
- **High concurrency** → `asyncio` shines

### 📈 **Next Steps:**
- ✅ **Concurrency expert?** → Master [Advanced Features](../08_python_features/)
- 🔍 **See examples?** → Run [asyncio_example.py](./examples/asyncio_example.py)
- 📚 **Deep dive?** → Read the [concurrency docs](./docs/)

### 🔍 **Answer Key:**
*Test your Python concurrency mastery!*

<details>
<summary>🔓 Show Answers</summary>

1. **B** - `threading` module handles multithreading
2. **A** - `async def` defines asynchronous functions  
3. **A** - GIL (Global Interpreter Lock) limits Python threading
4. **B** - Multiprocessing for CPU-bound, threading for I/O-bound
5. **A** - `await` pauses until the awaited result is ready
6. **B** - `asyncio.gather()` runs multiple tasks concurrently

**🔥 Pro insights:**
- **GIL Impact:** Threading good for I/O, not CPU computation
- **Asyncio Magic:** Single-threaded but handles thousands of connections
- **Go vs Python:** Go's goroutines vs Python's async/await + GIL

</details>

---

*⚡ **Speed matters:** Choose the right concurrency model for the job!* ✨🐍 

## 🌟 Expert Challenge

**Question**: Create a hybrid concurrency framework that combines Python's asyncio with Go-like channels and Java's ExecutorService. Your solution should:

1. Implement a channel system that:
   - Supports both sync and async operations
   - Handles buffered and unbuffered channels
   - Provides select-like functionality
   - Manages backpressure

2. Create a worker pool that:
   - Combines threads and asyncio
   - Handles both CPU and I/O bound tasks
   - Provides graceful shutdown
   - Monitors worker health

**Hint**: Look into `asyncio.Queue`, `threading.Event`, `concurrent.futures`, and `contextvars`.

<details>
<summary>Show Answer</summary>

```python
import asyncio
import concurrent.futures
import contextlib
import enum
import queue
import threading
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Generic, List, Optional, Set, TypeVar, Union

T = TypeVar('T')

class ChannelClosed(Exception):
    """Raised when operating on a closed channel"""
    pass

class ChannelState(enum.Enum):
    OPEN = 'open'
    CLOSING = 'closing'
    CLOSED = 'closed'

@dataclass
class ChannelStats:
    queue_size: int
    waiters: int
    state: ChannelState

class Channel(Generic[T]):
    def __init__(self, maxsize: int = 0):
        self._queue: asyncio.Queue[T] = asyncio.Queue(maxsize)
        self._sync_queue: queue.Queue[T] = queue.Queue(maxsize)
        self._state = ChannelState.OPEN
        self._lock = threading.Lock()
        self._waiters: Set[asyncio.Future] = set()
        self._loop = asyncio.get_event_loop()
    
    def stats(self) -> ChannelStats:
        return ChannelStats(
            queue_size=self._queue.qsize(),
            waiters=len(self._waiters),
            state=self._state
        )
    
    async def async_put(self, item: T) -> None:
        if self._state != ChannelState.OPEN:
            raise ChannelClosed()
        
        await self._queue.put(item)
        
        # Notify sync waiters
        try:
            self._sync_queue.put_nowait(item)
        except queue.Full:
            pass
    
    def sync_put(self, item: T, timeout: Optional[float] = None) -> None:
        if self._state != ChannelState.OPEN:
            raise ChannelClosed()
        
        self._sync_queue.put(item, timeout=timeout)
        
        # Schedule async put
        async def _put():
            await self._queue.put(item)
        
        asyncio.run_coroutine_threadsafe(_put(), self._loop)
    
    async def async_get(self) -> T:
        if self._state == ChannelState.CLOSED and self._queue.empty():
            raise ChannelClosed()
        
        waiter = self._loop.create_future()
        self._waiters.add(waiter)
        
        try:
            return await self._queue.get()
        finally:
            self._waiters.remove(waiter)
            self._queue.task_done()
    
    def sync_get(self, timeout: Optional[float] = None) -> T:
        if self._state == ChannelState.CLOSED and self._sync_queue.empty():
            raise ChannelClosed()
        
        return self._sync_queue.get(timeout=timeout)
    
    async def close(self) -> None:
        with self._lock:
            if self._state != ChannelState.OPEN:
                return
            
            self._state = ChannelState.CLOSING
            
            # Wait for queue to drain
            await self._queue.join()
            
            self._state = ChannelState.CLOSED
            
            # Cancel all waiters
            for waiter in self._waiters:
                if not waiter.done():
                    waiter.set_exception(ChannelClosed())

class WorkerPool:
    def __init__(
        self,
        num_threads: int,
        num_async_workers: int,
        queue_size: int = 0
    ):
        self._thread_executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=num_threads
        )
        self._process_executor = concurrent.futures.ProcessPoolExecutor(
            max_workers=num_threads
        )
        self._num_async_workers = num_async_workers
        self._tasks: Dict[str, asyncio.Task] = {}
        self._channels: Dict[str, Channel] = {}
        self._stop_event = asyncio.Event()
        self._queue = Channel[Callable](queue_size)
    
    async def start(self):
        # Start async workers
        for i in range(self._num_async_workers):
            task = asyncio.create_task(self._async_worker(f"async_worker_{i}"))
            self._tasks[f"async_worker_{i}"] = task
        
        # Start monitoring task
        monitor = asyncio.create_task(self._monitor_workers())
        self._tasks["monitor"] = monitor
    
    async def _async_worker(self, name: str):
        while not self._stop_event.is_set():
            try:
                task = await self._queue.async_get()
                if asyncio.iscoroutinefunction(task):
                    await task()
                else:
                    # CPU-bound task, run in process pool
                    await asyncio.get_event_loop().run_in_executor(
                        self._process_executor, task
                    )
            except ChannelClosed:
                break
            except Exception as e:
                print(f"Worker {name} error: {e}")
    
    async def _monitor_workers(self):
        while not self._stop_event.is_set():
            # Check worker health
            for name, task in list(self._tasks.items()):
                if task.done():
                    if exc := task.exception():
                        print(f"Worker {name} died with error: {exc}")
                        # Restart worker
                        if name.startswith("async_worker"):
                            new_task = asyncio.create_task(
                                self._async_worker(name)
                            )
                            self._tasks[name] = new_task
            
            await asyncio.sleep(1)
    
    async def submit(self, task: Callable):
        if self._stop_event.is_set():
            raise RuntimeError("WorkerPool is shutting down")
        
        await self._queue.async_put(task)
    
    def submit_sync(self, task: Callable, timeout: Optional[float] = None):
        if self._stop_event.is_set():
            raise RuntimeError("WorkerPool is shutting down")
        
        self._queue.sync_put(task, timeout=timeout)
    
    async def shutdown(self, timeout: Optional[float] = None):
        self._stop_event.set()
        await self._queue.close()
        
        if timeout is not None:
            try:
                await asyncio.wait_for(
                    asyncio.gather(*self._tasks.values()),
                    timeout
                )
            except asyncio.TimeoutError:
                print("Shutdown timed out, force closing...")
        else:
            await asyncio.gather(*self._tasks.values())
        
        self._thread_executor.shutdown(wait=True)
        self._process_executor.shutdown(wait=True)

# Usage example:
async def main():
    # Create a worker pool with 4 threads and 2 async workers
    pool = WorkerPool(4, 2)
    await pool.start()
    
    # CPU-bound task
    def cpu_task():
        result = sum(i * i for i in range(1000000))
        print(f"CPU task result: {result}")
    
    # I/O-bound task
    async def io_task():
        await asyncio.sleep(1)
        print("I/O task completed")
    
    # Submit tasks
    await pool.submit(cpu_task)
    await pool.submit(io_task)
    
    # Submit from another thread
    def thread_task():
        pool.submit_sync(cpu_task)
    
    thread = threading.Thread(target=thread_task)
    thread.start()
    thread.join()
    
    # Graceful shutdown
    await pool.shutdown(timeout=5)

if __name__ == "__main__":
    asyncio.run(main())
```

Key differences from Go/Java:
1. Python combines multiple concurrency models (threads, processes, async)
2. Channels need explicit synchronization between sync/async code
3. Worker pools are more complex due to the GIL
4. Graceful shutdown requires careful coordination
5. Error handling is more explicit than Go's panic/recover
6. Resource cleanup needs manual management (no `defer`)
7. Process pools handle CPU-bound tasks (vs Go's goroutines)

</details>