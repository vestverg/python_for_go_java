# ⚡ Concurrency in Python

## 📖 Introduction

This section explores Python's concurrency features, including threading, multiprocessing, and asynchronous programming. Python's approach to concurrency differs significantly from Java and Go, with unique characteristics due to the Global Interpreter Lock (GIL) and its async/await syntax.

## Understanding Python's Concurrency Model

### The Global Interpreter Lock (GIL)

Python's GIL is a mutex that protects access to Python objects, preventing multiple native threads from executing Python bytecodes simultaneously. This has important implications:

```python
import threading
import time
from typing import List

def cpu_bound_task(n: int) -> int:
    """CPU-intensive task that demonstrates GIL limitations."""
    total = 0
    for i in range(n):
        total += i * i
    return total

def demonstrate_gil_impact():
    """Show how GIL affects CPU-bound tasks."""
    start_time = time.time()
    
    # Sequential execution
    result1 = cpu_bound_task(1000000)
    result2 = cpu_bound_task(1000000)
    sequential_time = time.time() - start_time
    
    # Threaded execution
    start_time = time.time()
    threads = []
    results = []
    
    def worker(n: int, results: List[int], index: int):
        results.append(cpu_bound_task(n))
    
    results = [None, None]
    t1 = threading.Thread(target=worker, args=(1000000, results, 0))
    t2 = threading.Thread(target=worker, args=(1000000, results, 1))
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    threaded_time = time.time() - start_time
    
    print(f"Sequential time: {sequential_time:.2f}s")
    print(f"Threaded time: {threaded_time:.2f}s")
    print(f"Speedup: {sequential_time / threaded_time:.2f}x")
```

## Threading

### Basic Threading

```python
import threading
import time
import queue
from typing import Any, Callable, Optional
import logging

# Configure logging for thread demonstration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WorkerThread(threading.Thread):
    """Custom thread class with enhanced functionality."""
    
    def __init__(
        self,
        target: Callable,
        args: tuple = (),
        kwargs: dict = None,
        name: Optional[str] = None
    ) -> None:
        super().__init__(target=target, args=args, kwargs=kwargs or {}, name=name)
        self.result: Any = None
        self.exception: Optional[Exception] = None
        self.daemon = True  # Dies when main thread dies
    
    def run(self) -> None:
        """Execute the target function and capture result/exception."""
        try:
            if self._target:
                self.result = self._target(*self._args, **self._kwargs)
        except Exception as e:
            self.exception = e
            logger.error(f"Thread {self.name} failed: {e}")
    
    def get_result(self, timeout: Optional[float] = None) -> Any:
        """Get the result of the thread execution."""
        self.join(timeout)
        if self.exception:
            raise self.exception
        return self.result


def io_bound_task(task_id: int, duration: float) -> str:
    """Simulate I/O-bound task."""
    logger.info(f"Task {task_id} starting")
    time.sleep(duration)  # Simulate I/O wait
    result = f"Task {task_id} completed after {duration}s"
    logger.info(result)
    return result


def demonstrate_basic_threading():
    """Demonstrate basic threading concepts."""
    threads = []
    
    # Create and start multiple threads
    for i in range(3):
        thread = WorkerThread(
            target=io_bound_task,
            args=(i, 1.0),
            name=f"Worker-{i}"
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    results = []
    for thread in threads:
        try:
            result = thread.get_result(timeout=5.0)
            results.append(result)
        except Exception as e:
            logger.error(f"Thread failed: {e}")
    
    return results
```

### Thread Synchronization

```python
import threading
import time
import random
from typing import List, Optional
from contextlib import contextmanager

class ThreadSafeCounter:
    """Thread-safe counter using locks."""
    
    def __init__(self) -> None:
        self._value = 0
        self._lock = threading.Lock()
    
    def increment(self) -> None:
        """Thread-safe increment."""
        with self._lock:
            self._value += 1
    
    def decrement(self) -> None:
        """Thread-safe decrement."""
        with self._lock:
            self._value -= 1
    
    @property
    def value(self) -> int:
        """Get current value."""
        with self._lock:
            return self._value


class BoundedBuffer:
    """Thread-safe bounded buffer using condition variables."""
    
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.buffer: List[Any] = []
        self.condition = threading.Condition()
    
    def put(self, item: Any, timeout: Optional[float] = None) -> bool:
        """Add item to buffer."""
        with self.condition:
            # Wait for space in buffer
            if not self.condition.wait_for(
                lambda: len(self.buffer) < self.capacity,
                timeout=timeout
            ):
                return False  # Timeout
            
            self.buffer.append(item)
            logger.info(f"Added {item} to buffer (size: {len(self.buffer)})")
            
            # Notify waiting consumers
            self.condition.notify()
            return True
    
    def get(self, timeout: Optional[float] = None) -> Optional[Any]:
        """Remove and return item from buffer."""
        with self.condition:
            # Wait for item in buffer
            if not self.condition.wait_for(
                lambda: len(self.buffer) > 0,
                timeout=timeout
            ):
                return None  # Timeout
            
            item = self.buffer.pop(0)
            logger.info(f"Removed {item} from buffer (size: {len(self.buffer)})")
            
            # Notify waiting producers
            self.condition.notify()
            return item


class ReadWriteLock:
    """Read-write lock implementation."""
    
    def __init__(self) -> None:
        self._read_ready = threading.Condition(threading.RLock())
        self._readers = 0
    
    @contextmanager
    def read_lock(self):
        """Context manager for read lock."""
        self.acquire_read()
        try:
            yield
        finally:
            self.release_read()
    
    @contextmanager
    def write_lock(self):
        """Context manager for write lock."""
        self.acquire_write()
        try:
            yield
        finally:
            self.release_write()
    
    def acquire_read(self) -> None:
        """Acquire read lock."""
        with self._read_ready:
            self._readers += 1
    
    def release_read(self) -> None:
        """Release read lock."""
        with self._read_ready:
            self._readers -= 1
            if self._readers == 0:
                self._read_ready.notify_all()
    
    def acquire_write(self) -> None:
        """Acquire write lock."""
        self._read_ready.acquire()
        while self._readers > 0:
            self._read_ready.wait()
    
    def release_write(self) -> None:
        """Release write lock."""
        self._read_ready.release()


def producer_consumer_example():
    """Demonstrate producer-consumer pattern."""
    buffer = BoundedBuffer(capacity=5)
    
    def producer(producer_id: int, items: int):
        """Producer function."""
        for i in range(items):
            item = f"P{producer_id}-Item{i}"
            if buffer.put(item, timeout=2.0):
                time.sleep(random.uniform(0.1, 0.5))
            else:
                logger.warning(f"Producer {producer_id} timed out")
    
    def consumer(consumer_id: int, items: int):
        """Consumer function."""
        for i in range(items):
            item = buffer.get(timeout=2.0)
            if item:
                logger.info(f"Consumer {consumer_id} processed {item}")
                time.sleep(random.uniform(0.1, 0.5))
            else:
                logger.warning(f"Consumer {consumer_id} timed out")
    
    # Create producers and consumers
    threads = []
    
    # 2 producers, each producing 5 items
    for i in range(2):
        t = threading.Thread(target=producer, args=(i, 5))
        threads.append(t)
        t.start()
    
    # 2 consumers, each consuming 5 items
    for i in range(2):
        t = threading.Thread(target=consumer, args=(i, 5))
        threads.append(t)
        t.start()
    
    # Wait for all threads
    for t in threads:
        t.join()
```

### Thread Pool Executor

```python
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from typing import List, Callable, Any, Iterable
import requests
import time

class ThreadPoolManager:
    """Enhanced thread pool manager."""
    
    def __init__(self, max_workers: int = 4) -> None:
        self.max_workers = max_workers
    
    def execute_parallel(
        self,
        func: Callable,
        args_list: List[tuple],
        timeout: Optional[float] = None
    ) -> List[Any]:
        """Execute function with different arguments in parallel."""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_args = {
                executor.submit(func, *args): args
                for args in args_list
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_args, timeout=timeout):
                args = future_to_args[future]
                try:
                    result = future.result()
                    results.append((args, result, None))
                except Exception as e:
                    results.append((args, None, e))
        
        return results
    
    def map_parallel(
        self,
        func: Callable,
        iterable: Iterable,
        timeout: Optional[float] = None
    ) -> List[Any]:
        """Map function over iterable in parallel."""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            return list(executor.map(func, iterable, timeout=timeout))


def fetch_url(url: str) -> dict:
    """Fetch URL and return response info."""
    start_time = time.time()
    try:
        response = requests.get(url, timeout=5)
        return {
            'url': url,
            'status_code': response.status_code,
            'content_length': len(response.content),
            'response_time': time.time() - start_time,
            'success': True
        }
    except Exception as e:
        return {
            'url': url,
            'error': str(e),
            'response_time': time.time() - start_time,
            'success': False
        }


def demonstrate_thread_pool():
    """Demonstrate thread pool usage."""
    urls = [
        'https://httpbin.org/delay/1',
        'https://httpbin.org/delay/2',
        'https://httpbin.org/delay/1',
        'https://httpbin.org/status/200',
        'https://httpbin.org/status/404',
    ]
    
    pool_manager = ThreadPoolManager(max_workers=3)
    
    # Measure sequential execution
    start_time = time.time()
    sequential_results = [fetch_url(url) for url in urls]
    sequential_time = time.time() - start_time
    
    # Measure parallel execution
    start_time = time.time()
    parallel_results = pool_manager.map_parallel(fetch_url, urls, timeout=10)
    parallel_time = time.time() - start_time
    
    print(f"Sequential time: {sequential_time:.2f}s")
    print(f"Parallel time: {parallel_time:.2f}s")
    print(f"Speedup: {sequential_time / parallel_time:.2f}x")
    
    return parallel_results
```

## Multiprocessing

### Basic Multiprocessing

```python
import multiprocessing as mp
import time
import math
from typing import List, Tuple, Any
import logging

def cpu_intensive_task(n: int) -> Tuple[int, float]:
    """CPU-intensive task that benefits from multiprocessing."""
    start_time = time.time()
    
    # Calculate prime numbers up to n
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    
    execution_time = time.time() - start_time
    return len(primes), execution_time


class MultiprocessingManager:
    """Manager for multiprocessing operations."""
    
    def __init__(self, processes: Optional[int] = None) -> None:
        self.processes = processes or mp.cpu_count()
    
    def execute_parallel(
        self,
        func: Callable,
        args_list: List[Any],
        timeout: Optional[float] = None
    ) -> List[Any]:
        """Execute function with different arguments in parallel processes."""
        with mp.Pool(processes=self.processes) as pool:
            try:
                if timeout:
                    result = pool.map_async(func, args_list)
                    return result.get(timeout=timeout)
                else:
                    return pool.map(func, args_list)
            except mp.TimeoutError:
                pool.terminate()
                pool.join()
                raise
    
    def starmap_parallel(
        self,
        func: Callable,
        args_list: List[tuple],
        timeout: Optional[float] = None
    ) -> List[Any]:
        """Execute function with tuple arguments in parallel processes."""
        with mp.Pool(processes=self.processes) as pool:
            try:
                if timeout:
                    result = pool.starmap_async(func, args_list)
                    return result.get(timeout=timeout)
                else:
                    return pool.starmap(func, args_list)
            except mp.TimeoutError:
                pool.terminate()
                pool.join()
                raise


def worker_process(task_queue: mp.Queue, result_queue: mp.Queue, worker_id: int):
    """Worker process for queue-based processing."""
    logger.info(f"Worker {worker_id} starting")
    
    while True:
        try:
            # Get task from queue (blocks until available)
            task = task_queue.get(timeout=1)
            if task is None:  # Poison pill to stop worker
                break
            
            # Process task
            task_id, data = task
            result = cpu_intensive_task(data)
            
            # Put result in result queue
            result_queue.put((worker_id, task_id, result))
            
        except Exception as e:
            logger.error(f"Worker {worker_id} error: {e}")
            break
    
    logger.info(f"Worker {worker_id} finished")


def demonstrate_multiprocessing():
    """Demonstrate different multiprocessing approaches."""
    tasks = [1000, 2000, 3000, 4000, 5000]
    
    # Approach 1: Pool.map
    print("Using Pool.map:")
    manager = MultiprocessingManager(processes=4)
    
    start_time = time.time()
    results = manager.execute_parallel(cpu_intensive_task, tasks, timeout=30)
    pool_time = time.time() - start_time
    
    print(f"Pool execution time: {pool_time:.2f}s")
    for i, (count, exec_time) in enumerate(results):
        print(f"Task {i}: Found {count} primes in {exec_time:.2f}s")
    
    # Approach 2: Manual process management with queues
    print("\nUsing manual process management:")
    
    task_queue = mp.Queue()
    result_queue = mp.Queue()
    
    # Add tasks to queue
    for i, task_data in enumerate(tasks):
        task_queue.put((i, task_data))
    
    # Create worker processes
    processes = []
    num_workers = 4
    
    start_time = time.time()
    
    for worker_id in range(num_workers):
        p = mp.Process(target=worker_process, args=(task_queue, result_queue, worker_id))
        p.start()
        processes.append(p)
    
    # Add poison pills to stop workers
    for _ in range(num_workers):
        task_queue.put(None)
    
    # Collect results
    results = []
    for _ in range(len(tasks)):
        results.append(result_queue.get())
    
    # Wait for all processes to finish
    for p in processes:
        p.join()
    
    manual_time = time.time() - start_time
    print(f"Manual execution time: {manual_time:.2f}s")
    
    # Sort results by task_id
    results.sort(key=lambda x: x[1])
    for worker_id, task_id, (count, exec_time) in results:
        print(f"Worker {worker_id}, Task {task_id}: Found {count} primes in {exec_time:.2f}s")
```

### Process Communication

```python
import multiprocessing as mp
import time
import random
from typing import Any, Optional
import queue

class ProcessSafeCounter:
    """Process-safe counter using multiprocessing.Value."""
    
    def __init__(self) -> None:
        self._value = mp.Value('i', 0)  # 'i' for integer
        self._lock = mp.Lock()
    
    def increment(self) -> None:
        """Thread and process-safe increment."""
        with self._lock:
            self._value.value += 1
    
    def get_value(self) -> int:
        """Get current value."""
        with self._lock:
            return self._value.value


class SharedDataProcessor:
    """Demonstrate shared memory between processes."""
    
    def __init__(self, array_size: int) -> None:
        # Shared array of doubles
        self.shared_array = mp.Array('d', array_size)
        self.array_size = array_size
        self.lock = mp.Lock()
    
    def initialize_array(self) -> None:
        """Initialize shared array with random values."""
        with self.lock:
            for i in range(self.array_size):
                self.shared_array[i] = random.uniform(0, 100)
    
    def process_chunk(self, start: int, end: int, multiplier: float) -> None:
        """Process a chunk of the shared array."""
        with self.lock:
            for i in range(start, min(end, self.array_size)):
                self.shared_array[i] *= multiplier
    
    def get_array_copy(self) -> List[float]:
        """Get a copy of the shared array."""
        with self.lock:
            return list(self.shared_array[:])


def process_worker(
    shared_processor: SharedDataProcessor,
    start: int,
    end: int,
    multiplier: float,
    worker_id: int
) -> None:
    """Worker process for shared data processing."""
    logger.info(f"Worker {worker_id} processing range {start}-{end}")
    shared_processor.process_chunk(start, end, multiplier)
    logger.info(f"Worker {worker_id} completed")


def demonstrate_shared_memory():
    """Demonstrate shared memory between processes."""
    array_size = 1000
    num_processes = 4
    multiplier = 2.0
    
    # Create shared data processor
    processor = SharedDataProcessor(array_size)
    processor.initialize_array()
    
    print("Initial array (first 10 elements):")
    initial_array = processor.get_array_copy()
    print(initial_array[:10])
    
    # Calculate chunk size for each process
    chunk_size = array_size // num_processes
    
    # Create processes
    processes = []
    for i in range(num_processes):
        start = i * chunk_size
        end = start + chunk_size if i < num_processes - 1 else array_size
        
        p = mp.Process(
            target=process_worker,
            args=(processor, start, end, multiplier, i)
        )
        processes.append(p)
        p.start()
    
    # Wait for all processes to complete
    for p in processes:
        p.join()
    
    print("\nFinal array (first 10 elements):")
    final_array = processor.get_array_copy()
    print(final_array[:10])
    
    # Verify results
    expected = [x * multiplier for x in initial_array]
    assert abs(sum(final_array) - sum(expected)) < 1e-10
    print("Shared memory processing completed successfully!")


class ProcessManager:
    """Advanced process manager with monitoring."""
    
    def __init__(self) -> None:
        self.manager = mp.Manager()
        self.status_dict = self.manager.dict()
        self.result_queue = mp.Queue()
    
    def monitored_worker(
        self,
        worker_id: int,
        task_func: Callable,
        *args,
        **kwargs
    ) -> None:
        """Worker with status monitoring."""
        try:
            self.status_dict[worker_id] = "starting"
            
            result = task_func(*args, **kwargs)
            
            self.status_dict[worker_id] = "completed"
            self.result_queue.put((worker_id, result, None))
            
        except Exception as e:
            self.status_dict[worker_id] = f"failed: {e}"
            self.result_queue.put((worker_id, None, e))
    
    def execute_with_monitoring(
        self,
        task_func: Callable,
        tasks: List[tuple],
        timeout: float = 60.0
    ) -> List[tuple]:
        """Execute tasks with real-time monitoring."""
        processes = []
        
        # Start processes
        for i, task_args in enumerate(tasks):
            p = mp.Process(
                target=self.monitored_worker,
                args=(i, task_func) + task_args
            )
            p.start()
            processes.append(p)
        
        # Monitor progress
        start_time = time.time()
        results = []
        
        while len(results) < len(tasks):
            if time.time() - start_time > timeout:
                # Terminate remaining processes
                for p in processes:
                    if p.is_alive():
                        p.terminate()
                break
            
            # Check for results
            try:
                result = self.result_queue.get(timeout=0.1)
                results.append(result)
            except queue.Empty:
                continue
            
            # Print status update
            completed = len(results)
            total = len(tasks)
            print(f"Progress: {completed}/{total} tasks completed")
        
        # Wait for all processes to finish
        for p in processes:
            p.join(timeout=1.0)
            if p.is_alive():
                p.terminate()
                p.join()
        
        return results
```

## Asynchronous Programming

### Basic Async/Await

```python
import asyncio
import aiohttp
import time
from typing import List, Dict, Any, Optional, Callable
import logging

class AsyncTaskManager:
    """Manager for asynchronous tasks."""
    
    def __init__(self) -> None:
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def fetch_url(self, url: str, timeout: float = 5.0) -> Dict[str, Any]:
        """Fetch URL asynchronously."""
        start_time = time.time()
        
        try:
            async with self.session.get(url, timeout=timeout) as response:
                content = await response.text()
                return {
                    'url': url,
                    'status': response.status,
                    'content_length': len(content),
                    'response_time': time.time() - start_time,
                    'success': True
                }
        except Exception as e:
            return {
                'url': url,
                'error': str(e),
                'response_time': time.time() - start_time,
                'success': False
            }
    
    async def fetch_multiple_urls(
        self,
        urls: List[str],
        concurrency_limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Fetch multiple URLs with concurrency limit."""
        semaphore = asyncio.Semaphore(concurrency_limit)
        
        async def fetch_with_semaphore(url: str) -> Dict[str, Any]:
            async with semaphore:
                return await self.fetch_url(url)
        
        tasks = [fetch_with_semaphore(url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)


async def async_producer(queue: asyncio.Queue, items: int, delay: float = 0.1):
    """Async producer coroutine."""
    for i in range(items):
        item = f"item-{i}"
        await queue.put(item)
        logger.info(f"Produced: {item}")
        await asyncio.sleep(delay)
    
    # Signal completion
    await queue.put(None)


async def async_consumer(
    queue: asyncio.Queue,
    consumer_id: int,
    process_delay: float = 0.2
):
    """Async consumer coroutine."""
    while True:
        item = await queue.get()
        if item is None:
            # Poison pill - put it back for other consumers
            await queue.put(None)
            break
        
        logger.info(f"Consumer {consumer_id} processing: {item}")
        await asyncio.sleep(process_delay)  # Simulate processing
        queue.task_done()


async def demonstrate_async_patterns():
    """Demonstrate various async patterns."""
    
    # Pattern 1: Concurrent HTTP requests
    print("1. Concurrent HTTP requests:")
    urls = [
        'https://httpbin.org/delay/1',
        'https://httpbin.org/delay/2',
        'https://httpbin.org/json',
        'https://httpbin.org/uuid',
        'https://httpbin.org/user-agent',
    ]
    
    async with AsyncTaskManager() as manager:
        start_time = time.time()
        results = await manager.fetch_multiple_urls(urls, concurrency_limit=3)
        async_time = time.time() - start_time
        
        print(f"Fetched {len(results)} URLs in {async_time:.2f}s")
        for result in results:
            if isinstance(result, dict) and result.get('success'):
                print(f"  {result['url']}: {result['status']} ({result['response_time']:.2f}s)")
    
    # Pattern 2: Producer-Consumer
    print("\n2. Async Producer-Consumer:")
    queue = asyncio.Queue(maxsize=5)
    
    # Create tasks
    producer_task = asyncio.create_task(async_producer(queue, 10, delay=0.1))
    consumer_tasks = [
        asyncio.create_task(async_consumer(queue, i, process_delay=0.3))
        for i in range(2)
    ]
    
    # Wait for producer to finish
    await producer_task
    
    # Wait for queue to be empty
    await queue.join()
    
    # Cancel consumers
    for task in consumer_tasks:
        task.cancel()
    
    await asyncio.gather(*consumer_tasks, return_exceptions=True)
    print("Producer-consumer pattern completed")


class AsyncRateLimiter:
    """Rate limiter for async operations."""
    
    def __init__(self, rate: float, burst: int = 1) -> None:
        self.rate = rate  # requests per second
        self.burst = burst  # maximum burst size
        self.tokens = burst
        self.last_update = time.time()
        self.lock = asyncio.Lock()
    
    async def acquire(self) -> None:
        """Acquire a token (rate limit)."""
        async with self.lock:
            now = time.time()
            
            # Add tokens based on elapsed time
            elapsed = now - self.last_update
            self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
            self.last_update = now
            
            # Wait if no tokens available
            if self.tokens < 1:
                wait_time = (1 - self.tokens) / self.rate
                await asyncio.sleep(wait_time)
                self.tokens = 0
            else:
                self.tokens -= 1


class AsyncWorkerPool:
    """Pool of async workers for task processing."""
    
    def __init__(self, num_workers: int = 10) -> None:
        self.num_workers = num_workers
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.workers: List[asyncio.Task] = []
        self.results: List[Any] = []
        self.running = False
    
    async def worker(self, worker_id: int) -> None:
        """Worker coroutine."""
        while self.running:
            try:
                # Get task with timeout
                task_func, args, kwargs = await asyncio.wait_for(
                    self.task_queue.get(),
                    timeout=1.0
                )
                
                # Execute task
                if asyncio.iscoroutinefunction(task_func):
                    result = await task_func(*args, **kwargs)
                else:
                    result = task_func(*args, **kwargs)
                
                self.results.append((worker_id, result, None))
                self.task_queue.task_done()
                
            except asyncio.TimeoutError:
                continue  # Check if still running
            except Exception as e:
                self.results.append((worker_id, None, e))
                self.task_queue.task_done()
    
    async def start(self) -> None:
        """Start the worker pool."""
        self.running = True
        self.workers = [
            asyncio.create_task(self.worker(i))
            for i in range(self.num_workers)
        ]
    
    async def stop(self) -> None:
        """Stop the worker pool."""
        self.running = False
        await asyncio.gather(*self.workers, return_exceptions=True)
    
    async def submit(self, func: Callable, *args, **kwargs) -> None:
        """Submit a task to the pool."""
        await self.task_queue.put((func, args, kwargs))
    
    async def wait_for_completion(self) -> None:
        """Wait for all tasks to complete."""
        await self.task_queue.join()


async def demonstrate_advanced_async():
    """Demonstrate advanced async patterns."""
    
    # Rate limiting example
    print("Rate limiting example:")
    rate_limiter = AsyncRateLimiter(rate=2.0, burst=3)  # 2 requests per second
    
    async def rate_limited_operation(operation_id: int) -> str:
        await rate_limiter.acquire()
        start_time = time.time()
        await asyncio.sleep(0.1)  # Simulate work
        return f"Operation {operation_id} completed at {start_time:.2f}"
    
    # Submit multiple operations
    start_time = time.time()
    tasks = [rate_limited_operation(i) for i in range(5)]
    results = await asyncio.gather(*tasks)
    total_time = time.time() - start_time
    
    for result in results:
        print(f"  {result}")
    print(f"Total time: {total_time:.2f}s (should be ~2s due to rate limiting)")
    
    # Worker pool example
    print("\nWorker pool example:")
    
    async def async_work(item: int) -> int:
        await asyncio.sleep(0.1)  # Simulate async work
        return item * item
    
    pool = AsyncWorkerPool(num_workers=3)
    await pool.start()
    
    # Submit tasks
    for i in range(10):
        await pool.submit(async_work, i)
    
    # Wait for completion
    await pool.wait_for_completion()
    await pool.stop()
    
    # Print results
    pool.results.sort(key=lambda x: x[1] if x[2] is None else -1)
    for worker_id, result, error in pool.results:
        if error:
            print(f"  Worker {worker_id}: Error - {error}")
        else:
            print(f"  Worker {worker_id}: Result - {result}")
```

## Performance Comparison

```python
import time
import asyncio
import threading
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import List, Callable, Any

def cpu_bound_work(n: int) -> int:
    """CPU-intensive work."""
    total = 0
    for i in range(n):
        total += i * i
    return total

def io_bound_work(delay: float) -> str:
    """I/O-intensive work simulation."""
    time.sleep(delay)
    return f"Completed after {delay}s"

async def async_io_work(delay: float) -> str:
    """Async I/O work simulation."""
    await asyncio.sleep(delay)
    return f"Async completed after {delay}s"

class PerformanceComparator:
    """Compare performance of different concurrency approaches."""
    
    @staticmethod
    def time_execution(func: Callable, *args, **kwargs) -> tuple:
        """Time the execution of a function."""
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        return result, execution_time
    
    @staticmethod
    async def time_async_execution(coro_func: Callable, *args, **kwargs) -> tuple:
        """Time the execution of an async function."""
        start_time = time.time()
        result = await coro_func(*args, **kwargs)
        execution_time = time.time() - start_time
        return result, execution_time
    
    def compare_cpu_bound(self, tasks: List[int]) -> dict:
        """Compare CPU-bound task performance."""
        results = {}
        
        # Sequential
        _, results['sequential'] = self.time_execution(
            lambda: [cpu_bound_work(task) for task in tasks]
        )
        
        # Threading (should be slow due to GIL)
        def threaded_cpu():
            with ThreadPoolExecutor(max_workers=4) as executor:
                return list(executor.map(cpu_bound_work, tasks))
        
        _, results['threading'] = self.time_execution(threaded_cpu)
        
        # Multiprocessing (should be fast)
        def multiprocess_cpu():
            with ProcessPoolExecutor(max_workers=4) as executor:
                return list(executor.map(cpu_bound_work, tasks))
        
        _, results['multiprocessing'] = self.time_execution(multiprocess_cpu)
        
        return results
    
    async def compare_io_bound(self, delays: List[float]) -> dict:
        """Compare I/O-bound task performance."""
        results = {}
        
        # Sequential
        _, results['sequential'] = await self.time_async_execution(
            lambda: [io_bound_work(delay) for delay in delays]
        )
        
        # Threading
        def threaded_io():
            with ThreadPoolExecutor(max_workers=4) as executor:
                return list(executor.map(io_bound_work, delays))
        
        _, results['threading'] = await self.time_async_execution(
            lambda: asyncio.get_event_loop().run_in_executor(None, threaded_io)
        )
        
        # Async
        _, results['async'] = await self.time_async_execution(
            lambda: asyncio.gather(*[async_io_work(delay) for delay in delays])
        )
        
        return results

def run_performance_comparison():
    """Run comprehensive performance comparison."""
    comparator = PerformanceComparator()
    
    print("CPU-bound task comparison:")
    cpu_tasks = [100000] * 4  # 4 CPU-intensive tasks
    cpu_results = comparator.compare_cpu_bound(cpu_tasks)
    
    for method, time_taken in cpu_results.items():
        print(f"  {method}: {time_taken:.2f}s")
    
    print(f"  Multiprocessing speedup: {cpu_results['sequential'] / cpu_results['multiprocessing']:.1f}x")
    
    print("\nI/O-bound task comparison:")
    async def run_io_comparison():
        io_delays = [1.0] * 4  # 4 I/O tasks with 1s delay each
        io_results = await comparator.compare_io_bound(io_delays)
        
        for method, time_taken in io_results.items():
            print(f"  {method}: {time_taken:.2f}s")
        
        print(f"  Async speedup: {io_results['sequential'] / io_results['async']:.1f}x")
        print(f"  Threading speedup: {io_results['sequential'] / io_results['threading']:.1f}x")
    
    asyncio.run(run_io_comparison())

# Best Practices and Guidelines

## When to Use Each Approach

### Threading
- **Best for**: I/O-bound tasks (file operations, network requests, database queries)
- **Avoid for**: CPU-intensive computations (due to GIL)
- **Example use cases**: Web scraping, API calls, file processing

### Multiprocessing
- **Best for**: CPU-intensive tasks that can be parallelized
- **Consider**: Memory overhead and IPC costs
- **Example use cases**: Data processing, mathematical computations, image processing

### Async/Await
- **Best for**: I/O-bound tasks with many concurrent operations
- **Great for**: Network servers, concurrent API calls, real-time applications
- **Consider**: Learning curve and ecosystem maturity

## Common Pitfalls

### 1. Race Conditions
```python
# Wrong - race condition
counter = 0

def increment():
    global counter
    counter += 1  # Not atomic!

# Right - with lock
counter = 0
lock = threading.Lock()

def safe_increment():
    global counter
    with lock:
        counter += 1
```

### 2. Deadlocks
```python
# Wrong - potential deadlock
lock1 = threading.Lock()
lock2 = threading.Lock()

def thread1():
    with lock1:
        time.sleep(0.1)
        with lock2:
            pass

def thread2():
    with lock2:
        time.sleep(0.1)
        with lock1:
            pass

# Right - consistent lock ordering
def safe_thread1():
    with lock1:
        with lock2:
            pass

def safe_thread2():
    with lock1:
        with lock2:
            pass
```

### 3. Shared State Problems
```python
# Wrong - shared mutable state
shared_list = []

def worker(items):
    for item in items:
        shared_list.append(process(item))  # Race condition!

# Right - use return values and collect results
def safe_worker(items):
    return [process(item) for item in items]

# Collect results safely
with ThreadPoolExecutor() as executor:
    futures = [executor.submit(safe_worker, chunk) for chunk in chunks]
    all_results = []
    for future in futures:
        all_results.extend(future.result())
```

## Testing Concurrent Code

```python
import unittest
from unittest.mock import patch, Mock
import threading
import time

class TestConcurrentCode(unittest.TestCase):
    """Test cases for concurrent code."""
    
    def test_thread_safety(self):
        """Test thread-safe counter."""
        counter = ThreadSafeCounter()
        threads = []
        
        def increment_many():
            for _ in range(1000):
                counter.increment()
        
        # Start multiple threads
        for _ in range(10):
            t = threading.Thread(target=increment_many)
            threads.append(t)
            t.start()
        
        # Wait for completion
        for t in threads:
            t.join()
        
        # Verify result
        self.assertEqual(counter.value, 10000)
    
    def test_async_function(self):
        """Test async function."""
        async def async_test():
            manager = AsyncTaskManager()
            async with manager:
                result = await manager.fetch_url('https://httpbin.org/json')
                self.assertTrue(result['success'])
                self.assertEqual(result['status'], 200)
        
        asyncio.run(async_test())
    
    @patch('requests.get')
    def test_with_mocking(self, mock_get):
        """Test with mocked external dependencies."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'test content'
        mock_get.return_value = mock_response
        
        result = fetch_url('https://example.com')
        self.assertTrue(result['success'])
        self.assertEqual(result['status_code'], 200)
```

## Comparison with Java and Go

### Java Concurrency vs Python

| Feature | Java | Python |
|---------|------|---------|
| **Threading Model** | True preemptive threading | GIL-limited threading |
| **Thread Creation** | `new Thread()` or `Executor` | `threading.Thread` |
| **Synchronization** | `synchronized`, `ReentrantLock` | `threading.Lock`, `Condition` |
| **Concurrent Collections** | `ConcurrentHashMap`, etc. | `queue.Queue`, manual sync |
| **Future/Promise** | `CompletableFuture` | `concurrent.futures.Future` |
| **Actor Model** | Akka (library) | Not built-in |

### Go Concurrency vs Python

| Feature | Go | Python |
|---------|-----|---------|
| **Primary Model** | Goroutines + Channels | Threads/Async + Queues |
| **Lightweight Threads** | Goroutines (very cheap) | Async tasks (cheap) |
| **Communication** | Channels (`chan`) | Queues, shared memory |
| **Synchronization** | `sync.Mutex`, channels | `threading.Lock`, `asyncio.Lock` |
| **CPU Parallelism** | Built-in (no GIL) | Requires multiprocessing |
| **Select Statement** | `select {}` | `asyncio.select` (limited) |

## Additional Resources

1. **Official Documentation**
   - [Threading](https://docs.python.org/3/library/threading.html)
   - [Multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
   - [Asyncio](https://docs.python.org/3/library/asyncio.html)

2. **Advanced Topics**
   - [Concurrent Futures](https://docs.python.org/3/library/concurrent.futures.html)
   - [Queue](https://docs.python.org/3/library/queue.html)
   - [AsyncIO Patterns](https://docs.python.org/3/library/asyncio-task.html)

3. **External Libraries**
   - [aiohttp](https://docs.aiohttp.org/) - Async HTTP client/server
   - [celery](https://docs.celeryproject.org/) - Distributed task queue
   - [trio](https://trio.readthedocs.io/) - Alternative async library 