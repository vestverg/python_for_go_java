# Threading in Python

## 🎯 Overview

Python threading is ideal for I/O-bound tasks where the GIL is frequently released. This guide covers essential patterns for developers coming from Java and Go.

## 🧵 Basic Threading

### Creating and Managing Threads

```python
import threading
import time
from concurrent.futures import ThreadPoolExecutor

# Method 1: Function-based
def worker(name, delay):
    for i in range(3):
        print(f"{name}: Task {i+1}")
        time.sleep(delay)

thread = threading.Thread(target=worker, args=("Worker-1", 1))
thread.start()
thread.join()

# Method 2: Class-based (like Java)
class WorkerThread(threading.Thread):
    def __init__(self, name, delay):
        super().__init__()
        self.name = name
        self.delay = delay
    
    def run(self):
        for i in range(3):
            print(f"{self.name}: Task {i+1}")
            time.sleep(self.delay)

worker = WorkerThread("Worker-2", 1)
worker.start()
worker.join()
```

## 🔄 Thread Synchronization

### Locks and Thread Safety

```python
import threading

class ThreadSafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()
    
    def increment(self):
        with self._lock:
            self._value += 1
    
    @property
    def value(self):
        return self._value

# Producer-Consumer with Condition
class ProducerConsumer:
    def __init__(self):
        self.items = []
        self.condition = threading.Condition()
    
    def produce(self, item):
        with self.condition:
            self.items.append(item)
            print(f"Produced: {item}")
            self.condition.notify()
    
    def consume(self):
        with self.condition:
            while not self.items:
                self.condition.wait()
            item = self.items.pop(0)
            print(f"Consumed: {item}")
            return item
```

## 📦 Queue-Based Patterns

### Worker Pool with Queue

```python
import threading
import queue
import time

def worker(name, task_queue):
    while True:
        try:
            task = task_queue.get(timeout=2)
            print(f"{name} processing: {task}")
            time.sleep(1)  # Simulate work
            task_queue.task_done()
        except queue.Empty:
            break

# Create queue and workers
task_queue = queue.Queue()
workers = []

for i in range(3):
    t = threading.Thread(target=worker, args=(f"Worker-{i}", task_queue))
    workers.append(t)
    t.start()

# Add tasks
for i in range(10):
    task_queue.put(f"Task-{i}")

# Wait for completion
task_queue.join()
```

## 🎭 ThreadPoolExecutor (Recommended)

### Basic Usage

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

def fetch_url(url):
    response = requests.get(url, timeout=5)
    return url, response.status_code

urls = [
    "https://httpbin.org/delay/1",
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
]

# Method 1: map() - simple and ordered
with ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(fetch_url, urls)
    for url, status in results:
        print(f"{url}: {status}")

# Method 2: submit() - more control
with ThreadPoolExecutor(max_workers=3) as executor:
    future_to_url = {executor.submit(fetch_url, url): url for url in urls}
    
    for future in as_completed(future_to_url):
        url = future_to_url[future]
        try:
            result_url, status = future.result()
            print(f"{result_url}: {status}")
        except Exception as e:
            print(f"{url}: Error - {e}")
```

### Advanced Task Management

```python
from concurrent.futures import ThreadPoolExecutor, Future
from typing import List, Callable

class TaskManager:
    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.futures: List[Future] = []
    
    def submit_task(self, func: Callable, *args, **kwargs) -> Future:
        future = self.executor.submit(func, *args, **kwargs)
        self.futures.append(future)
        return future
    
    def wait_for_all(self, timeout: float = None):
        results = []
        errors = []
        
        for future in self.futures:
            try:
                result = future.result(timeout=timeout)
                results.append(result)
            except Exception as e:
                errors.append(e)
        
        return results, errors
    
    def shutdown(self):
        self.executor.shutdown(wait=True)
```

## 🛡️ Best Practices

### Thread-Local Storage

```python
import threading

thread_local_data = threading.local()

def init_thread_data():
    thread_local_data.name = threading.current_thread().name
    thread_local_data.counter = 0

def worker_function():
    init_thread_data()
    for i in range(5):
        thread_local_data.counter += 1
        print(f"{thread_local_data.name}: {thread_local_data.counter}")
```

### Avoiding Common Pitfalls

```python
# BAD: Race condition
shared_counter = 0
def bad_increment():
    global shared_counter
    for _ in range(100000):
        shared_counter += 1  # Not atomic!

# GOOD: Thread-safe
safe_counter = 0
counter_lock = threading.Lock()
def good_increment():
    global safe_counter
    for _ in range(100000):
        with counter_lock:
            safe_counter += 1

# BAD: Potential deadlock
lock1 = threading.Lock()
lock2 = threading.Lock()
def thread_a():
    with lock1:
        with lock2:  # Lock order matters
            pass

def thread_b():
    with lock2:
        with lock1:  # Different order = deadlock risk
            pass

# GOOD: Consistent lock ordering
def safe_thread_a():
    with lock1:  # Always acquire lock1 first
        with lock2:
            pass

def safe_thread_b():
    with lock1:  # Same order
        with lock2:
            pass
```

## 📊 When to Use Threading

### ✅ Good Use Cases
- **File I/O operations**
- **Network requests** 
- **Database queries**
- **External API calls**
- **User interface responsiveness**

### ❌ Poor Use Cases
- **CPU-intensive computations**
- **Mathematical operations**
- **Image/video processing**

## 🔗 Next Steps

- **For CPU-bound work**: [Multiprocessing →](03-multiprocessing.md)
- **For async patterns**: [AsyncIO →](04-async-await.md)
- **Performance tips**: [Performance Guide →](05-performance.md) 