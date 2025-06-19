# Multiprocessing in Python

## 🎯 Overview

Multiprocessing provides true parallelism by creating separate Python processes, each with its own interpreter and GIL. This is essential for CPU-bound tasks.

## 🚀 Basic Multiprocessing

### Process Creation

```python
import multiprocessing as mp
import time
import os

def worker_function(name, duration):
    """Worker function that runs in separate process"""
    print(f"Process {name} (PID: {os.getpid()}) starting...")
    time.sleep(duration)
    print(f"Process {name} completed")
    return f"Result from {name}"

# Method 1: Process class
process = mp.Process(target=worker_function, args=("Worker-1", 2))
process.start()
process.join()

# Method 2: Multiple processes
processes = []
for i in range(3):
    p = mp.Process(target=worker_function, args=(f"Worker-{i}", 1))
    processes.append(p)
    p.start()

for p in processes:
    p.join()
```

### Process Pools (Recommended)

```python
import multiprocessing as mp
import numpy as np

def cpu_intensive_task(matrix_size):
    """CPU-intensive matrix multiplication"""
    matrix_a = np.random.rand(matrix_size, matrix_size)
    matrix_b = np.random.rand(matrix_size, matrix_size)
    result = np.matmul(matrix_a, matrix_b)
    return matrix_size, result.shape

def main():
    matrix_sizes = [100, 200, 300, 400, 500]
    
    # Sequential processing
    start_time = time.time()
    sequential_results = [cpu_intensive_task(size) for size in matrix_sizes]
    sequential_time = time.time() - start_time
    
    # Parallel processing
    start_time = time.time()
    with mp.Pool() as pool:
        parallel_results = pool.map(cpu_intensive_task, matrix_sizes)
    parallel_time = time.time() - start_time
    
    print(f"Sequential: {sequential_time:.2f}s")
    print(f"Parallel: {parallel_time:.2f}s")
    print(f"Speedup: {sequential_time / parallel_time:.2f}x")

if __name__ == "__main__":
    main()
```

## 🔄 Inter-Process Communication

### Queues

```python
import multiprocessing as mp
import time
import random

def producer(queue, name):
    """Producer process"""
    for i in range(5):
        item = f"{name}-Item-{i}"
        queue.put(item)
        print(f"Produced: {item}")
        time.sleep(random.uniform(0.1, 0.5))

def consumer(queue, name):
    """Consumer process"""
    while True:
        try:
            item = queue.get(timeout=2)
            print(f"{name} consumed: {item}")
            time.sleep(random.uniform(0.2, 0.8))
        except:
            print(f"{name} timed out")
            break

def main():
    # Create queue
    queue = mp.Queue()
    
    # Start producer
    producer_process = mp.Process(target=producer, args=(queue, "Producer"))
    producer_process.start()
    
    # Start consumers
    consumer_processes = []
    for i in range(2):
        p = mp.Process(target=consumer, args=(queue, f"Consumer-{i}"))
        consumer_processes.append(p)
        p.start()
    
    # Wait for producer to finish
    producer_process.join()
    
    # Wait for consumers
    for p in consumer_processes:
        p.join()

if __name__ == "__main__":
    main()
```

### Shared Memory

```python
import multiprocessing as mp
import numpy as np
from multiprocessing import shared_memory

def worker_with_shared_array(shared_array, start_idx, end_idx):
    """Worker that modifies shared array"""
    # Modify slice of shared array
    for i in range(start_idx, end_idx):
        shared_array[i] = shared_array[i] ** 2

def main():
    # Create shared array
    size = 1000000
    shared_array = mp.Array('d', range(size))  # 'd' = double
    
    # Create processes to work on different slices
    num_processes = 4
    chunk_size = size // num_processes
    processes = []
    
    for i in range(num_processes):
        start_idx = i * chunk_size
        end_idx = start_idx + chunk_size if i < num_processes - 1 else size
        
        p = mp.Process(
            target=worker_with_shared_array,
            args=(shared_array, start_idx, end_idx)
        )
        processes.append(p)
        p.start()
    
    # Wait for all processes
    for p in processes:
        p.join()
    
    print(f"First 10 elements: {shared_array[:10]}")

if __name__ == "__main__":
    main()
```

### Pipes

```python
import multiprocessing as mp
import time

def sender(conn):
    """Send data through pipe"""
    for i in range(5):
        message = f"Message {i}"
        conn.send(message)
        print(f"Sent: {message}")
        time.sleep(1)
    conn.close()

def receiver(conn):
    """Receive data through pipe"""
    while True:
        try:
            message = conn.recv()
            print(f"Received: {message}")
        except EOFError:
            break

def main():
    # Create pipe
    parent_conn, child_conn = mp.Pipe()
    
    # Start processes
    sender_process = mp.Process(target=sender, args=(child_conn,))
    receiver_process = mp.Process(target=receiver, args=(parent_conn,))
    
    sender_process.start()
    receiver_process.start()
    
    sender_process.join()
    receiver_process.join()

if __name__ == "__main__":
    main()
```

## 🎭 Advanced Patterns

### Process Pool with Callback

```python
import multiprocessing as mp
import time

def cpu_task(n):
    """CPU-intensive task"""
    result = sum(i * i for i in range(n))
    return n, result

def task_complete(result):
    """Callback when task completes"""
    n, value = result
    print(f"Task {n} completed with result: {value}")

def error_callback(error):
    """Callback when task fails"""
    print(f"Task failed: {error}")

def main():
    with mp.Pool(processes=4) as pool:
        # Submit tasks with callbacks
        for i in range(1, 6):
            pool.apply_async(
                cpu_task, 
                args=(10000 * i,),
                callback=task_complete,
                error_callback=error_callback
            )
        
        # Close pool and wait
        pool.close()
        pool.join()

if __name__ == "__main__":
    main()
```

### Manager for Complex Shared Objects

```python
import multiprocessing as mp
import time

def worker(shared_dict, shared_list, name):
    """Worker that modifies shared objects"""
    # Modify shared dictionary
    shared_dict[name] = f"Process {name} was here"
    
    # Modify shared list
    shared_list.append(f"Entry from {name}")
    
    print(f"{name} updated shared objects")

def main():
    # Create manager
    with mp.Manager() as manager:
        # Create shared objects
        shared_dict = manager.dict()
        shared_list = manager.list()
        
        # Start processes
        processes = []
        for i in range(4):
            p = mp.Process(
                target=worker,
                args=(shared_dict, shared_list, f"Worker-{i}")
            )
            processes.append(p)
            p.start()
        
        # Wait for all processes
        for p in processes:
            p.join()
        
        print(f"Shared dict: {dict(shared_dict)}")
        print(f"Shared list: {list(shared_list)}")

if __name__ == "__main__":
    main()
```

## 🛡️ Best Practices

### Error Handling

```python
import multiprocessing as mp
import traceback

def safe_worker(task_data):
    """Worker with proper error handling"""
    try:
        # Simulate work that might fail
        if task_data < 0:
            raise ValueError("Negative input not allowed")
        
        result = task_data ** 2
        return {"success": True, "result": result, "task": task_data}
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "task": task_data
        }

def main():
    tasks = [1, 2, -3, 4, -5]  # Some will fail
    
    with mp.Pool() as pool:
        results = pool.map(safe_worker, tasks)
    
    # Process results
    for result in results:
        if result["success"]:
            print(f"Task {result['task']}: {result['result']}")
        else:
            print(f"Task {result['task']} failed: {result['error']}")

if __name__ == "__main__":
    main()
```

### Resource Management

```python
import multiprocessing as mp
import atexit

class ProcessManager:
    """Manages a pool of worker processes"""
    
    def __init__(self, num_processes=None):
        self.num_processes = num_processes or mp.cpu_count()
        self.pool = None
        self._start_pool()
    
    def _start_pool(self):
        """Start the process pool"""
        self.pool = mp.Pool(self.num_processes)
        atexit.register(self.cleanup)
    
    def submit_task(self, func, *args, **kwargs):
        """Submit task to pool"""
        if self.pool is None:
            raise RuntimeError("Pool is not running")
        return self.pool.apply_async(func, args, kwargs)
    
    def map_tasks(self, func, iterable):
        """Map function over iterable"""
        if self.pool is None:
            raise RuntimeError("Pool is not running")
        return self.pool.map(func, iterable)
    
    def cleanup(self):
        """Clean shutdown of pool"""
        if self.pool:
            self.pool.close()
            self.pool.join()
            self.pool = None
```

## 📊 Performance Considerations

### CPU-bound vs Memory-bound

```python
import multiprocessing as mp
import time
import psutil

def cpu_bound_task(n):
    """Pure CPU work"""
    total = 0
    for i in range(n):
        total += i ** 2
    return total

def memory_bound_task(size):
    """Memory-intensive work"""
    data = list(range(size))
    return sum(data)

def benchmark_task(task_func, args_list, task_name):
    """Benchmark sequential vs parallel execution"""
    # Sequential
    start = time.time()
    sequential_results = [task_func(arg) for arg in args_list]
    sequential_time = time.time() - start
    
    # Parallel
    start = time.time()
    with mp.Pool() as pool:
        parallel_results = pool.map(task_func, args_list)
    parallel_time = time.time() - start
    
    speedup = sequential_time / parallel_time
    print(f"{task_name}:")
    print(f"  Sequential: {sequential_time:.2f}s")
    print(f"  Parallel: {parallel_time:.2f}s")
    print(f"  Speedup: {speedup:.2f}x")
    print()

def main():
    cpu_args = [1000000] * 4
    memory_args = [10000000] * 4
    
    benchmark_task(cpu_bound_task, cpu_args, "CPU-bound")
    benchmark_task(memory_bound_task, memory_args, "Memory-bound")

if __name__ == "__main__":
    main()
```

## 🚫 Common Pitfalls

### Platform Considerations

```python
import multiprocessing as mp
import sys

# REQUIRED: Protect entry point on Windows
if __name__ == "__main__":
    # Set start method (Unix/Linux: fork, Windows: spawn)
    if sys.platform == "win32":
        mp.set_start_method("spawn")
    
    # Your multiprocessing code here
    pass

# BAD: No protection
def bad_example():
    with mp.Pool() as pool:
        results = pool.map(some_function, data)
    # This will create infinite processes on Windows!

# GOOD: Proper protection
def good_example():
    if __name__ == "__main__":
        with mp.Pool() as pool:
            results = pool.map(some_function, data)
```

## 🎯 When to Use Multiprocessing

### ✅ Perfect Use Cases
- **Mathematical computations**
- **Data processing and analysis**
- **Image/video processing**
- **Scientific simulations**
- **Cryptographic operations**

### ⚠️ Consider Alternatives
- **Small datasets** (overhead > benefit)
- **Memory-limited systems**
- **I/O-bound tasks** (use threading/asyncio)

## 🔗 Next Steps

- **For I/O-bound work**: [Threading →](02-threading.md)
- **For async patterns**: [AsyncIO →](04-async-await.md)
- **Performance optimization**: [Performance Guide →](05-performance.md) 