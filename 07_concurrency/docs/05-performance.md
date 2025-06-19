# Performance and Optimization

## 🎯 Overview

This guide covers performance optimization techniques for Python concurrency, benchmarking, and choosing the right approach for your use case.

## 📊 Performance Benchmarking

### Comparing Concurrency Models

```python
import asyncio
import time
import threading
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import requests
import aiohttp

def cpu_task(n):
    """CPU-intensive task"""
    return sum(i * i for i in range(n))

def io_task(url):
    """I/O-intensive task"""
    response = requests.get(url, timeout=5)
    return len(response.content)

async def async_io_task(session, url):
    """Async I/O task"""
    async with session.get(url) as response:
        content = await response.read()
        return len(content)

class PerformanceBenchmark:
    def __init__(self):
        self.urls = [
            "https://httpbin.org/delay/1",
            "https://httpbin.org/delay/1", 
            "https://httpbin.org/delay/1",
            "https://httpbin.org/delay/1",
        ]
        self.cpu_data = [100000] * 4
    
    def benchmark_cpu_sequential(self):
        start = time.time()
        results = [cpu_task(n) for n in self.cpu_data]
        return time.time() - start, len(results)
    
    def benchmark_cpu_threading(self):
        start = time.time()
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(cpu_task, self.cpu_data))
        return time.time() - start, len(results)
    
    def benchmark_cpu_multiprocessing(self):
        start = time.time()
        with ProcessPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(cpu_task, self.cpu_data))
        return time.time() - start, len(results)
    
    def benchmark_io_sequential(self):
        start = time.time()
        results = [io_task(url) for url in self.urls]
        return time.time() - start, len(results)
    
    def benchmark_io_threading(self):
        start = time.time()
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(io_task, self.urls))
        return time.time() - start, len(results)
    
    async def benchmark_io_asyncio(self):
        start = time.time()
        async with aiohttp.ClientSession() as session:
            tasks = [async_io_task(session, url) for url in self.urls]
            results = await asyncio.gather(*tasks)
        return time.time() - start, len(results)
    
    def run_all_benchmarks(self):
        print("🔄 CPU-bound Task Benchmarks:")
        
        elapsed, count = self.benchmark_cpu_sequential()
        print(f"Sequential: {elapsed:.2f}s")
        
        elapsed, count = self.benchmark_cpu_threading()
        print(f"Threading: {elapsed:.2f}s")
        
        elapsed, count = self.benchmark_cpu_multiprocessing()
        print(f"Multiprocessing: {elapsed:.2f}s")
        
        print("\n🌐 I/O-bound Task Benchmarks:")
        
        elapsed, count = self.benchmark_io_sequential()
        print(f"Sequential: {elapsed:.2f}s")
        
        elapsed, count = self.benchmark_io_threading()
        print(f"Threading: {elapsed:.2f}s")
        
        elapsed, count = asyncio.run(self.benchmark_io_asyncio())
        print(f"AsyncIO: {elapsed:.2f}s")

# Run benchmarks
if __name__ == "__main__":
    benchmark = PerformanceBenchmark()
    benchmark.run_all_benchmarks()
```

## 🎯 Choosing the Right Approach

### Decision Matrix

```python
import time
import psutil
import threading

class TaskProfiler:
    """Profile tasks to determine optimal concurrency model"""
    
    @staticmethod
    def profile_task(func, *args, **kwargs):
        """Profile a task to determine if it's CPU or I/O bound"""
        process = psutil.Process()
        
        # Measure before
        cpu_before = process.cpu_percent()
        memory_before = process.memory_info().rss
        start_time = time.time()
        
        # Run task
        result = func(*args, **kwargs)
        
        # Measure after
        end_time = time.time()
        cpu_after = process.cpu_percent()
        memory_after = process.memory_info().rss
        
        elapsed = end_time - start_time
        cpu_usage = max(cpu_after - cpu_before, 0)
        memory_delta = memory_after - memory_before
        
        # Determine task type
        if cpu_usage > 50:
            task_type = "CPU-bound"
            recommendation = "Use multiprocessing"
        elif elapsed > 0.1:  # Task takes time but low CPU
            task_type = "I/O-bound"
            recommendation = "Use threading or asyncio"
        else:
            task_type = "Quick task"
            recommendation = "Run sequentially"
        
        return {
            "type": task_type,
            "recommendation": recommendation,
            "cpu_usage": cpu_usage,
            "elapsed": elapsed,
            "memory_delta": memory_delta / 1024 / 1024  # MB
        }

# Example usage
def cpu_intensive():
    return sum(i ** 2 for i in range(1000000))

def io_simulation():
    time.sleep(0.5)
    return "I/O complete"

profiler = TaskProfiler()

print("CPU Task Profile:")
cpu_profile = profiler.profile_task(cpu_intensive)
print(f"Type: {cpu_profile['type']}")
print(f"Recommendation: {cpu_profile['recommendation']}")
print(f"CPU: {cpu_profile['cpu_usage']:.1f}%")
print(f"Time: {cpu_profile['elapsed']:.3f}s")

print("\nI/O Task Profile:")
io_profile = profiler.profile_task(io_simulation)
print(f"Type: {io_profile['type']}")
print(f"Recommendation: {io_profile['recommendation']}")
print(f"CPU: {io_profile['cpu_usage']:.1f}%")
print(f"Time: {io_profile['elapsed']:.3f}s")
```

## ⚡ Optimization Techniques

### Thread Pool Sizing

```python
import threading
import time
import math
from concurrent.futures import ThreadPoolExecutor

def find_optimal_thread_count(task_func, task_data, max_workers=20):
    """Find optimal thread count for I/O-bound tasks"""
    results = {}
    
    for workers in range(1, max_workers + 1):
        start = time.time()
        with ThreadPoolExecutor(max_workers=workers) as executor:
            list(executor.map(task_func, task_data))
        elapsed = time.time() - start
        results[workers] = elapsed
        print(f"Workers: {workers:2d}, Time: {elapsed:.2f}s")
    
    # Find optimal
    optimal_workers = min(results, key=results.get)
    print(f"\nOptimal thread count: {optimal_workers}")
    return optimal_workers

# Example I/O task
def io_task(duration):
    time.sleep(duration)
    return duration

# Find optimal thread count
task_data = [0.1] * 20  # 20 tasks, each taking 0.1 seconds
optimal = find_optimal_thread_count(io_task, task_data, max_workers=10)
```

### Memory Optimization

```python
import asyncio
import weakref
import gc

class MemoryOptimizedAsyncPool:
    """Memory-optimized async task pool"""
    
    def __init__(self, max_concurrent=100):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.active_tasks = weakref.WeakSet()
    
    async def run_task(self, coro):
        """Run task with memory management"""
        async with self.semaphore:
            task = asyncio.current_task()
            self.active_tasks.add(task)
            
            try:
                return await coro
            finally:
                # Force garbage collection periodically
                if len(self.active_tasks) % 50 == 0:
                    gc.collect()
    
    async def run_batch(self, coroutines):
        """Run batch of coroutines with memory management"""
        tasks = [self.run_task(coro) for coro in coroutines]
        return await asyncio.gather(*tasks)

# Usage example
async def memory_intensive_task(data_size):
    # Simulate memory-intensive work
    data = list(range(data_size))
    await asyncio.sleep(0.1)
    return len(data)

async def optimized_batch_processing():
    pool = MemoryOptimizedAsyncPool(max_concurrent=10)
    
    # Create many tasks
    coroutines = [memory_intensive_task(1000) for _ in range(100)]
    
    # Process in batches
    batch_size = 20
    results = []
    
    for i in range(0, len(coroutines), batch_size):
        batch = coroutines[i:i + batch_size]
        batch_results = await pool.run_batch(batch)
        results.extend(batch_results)
        
        # Optional: pause between batches
        await asyncio.sleep(0.01)
    
    return results

# Run optimized processing
results = asyncio.run(optimized_batch_processing())
print(f"Processed {len(results)} tasks with memory optimization")
```

## 📈 Monitoring and Profiling

### Performance Monitoring

```python
import time
import threading
import asyncio
import psutil
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class PerformanceMetrics:
    """Performance metrics container"""
    start_time: float
    end_time: float
    cpu_usage: float
    memory_usage: float
    task_count: int
    
    @property
    def elapsed_time(self):
        return self.end_time - self.start_time
    
    @property
    def throughput(self):
        return self.task_count / self.elapsed_time if self.elapsed_time > 0 else 0

class PerformanceMonitor:
    """Monitor performance of concurrent operations"""
    
    def __init__(self):
        self.metrics: List[PerformanceMetrics] = []
        self.process = psutil.Process()
    
    def start_monitoring(self, task_count: int):
        """Start performance monitoring"""
        return {
            'start_time': time.time(),
            'start_cpu': self.process.cpu_percent(),
            'start_memory': self.process.memory_info().rss,
            'task_count': task_count
        }
    
    def end_monitoring(self, start_data: Dict):
        """End performance monitoring and record metrics"""
        metrics = PerformanceMetrics(
            start_time=start_data['start_time'],
            end_time=time.time(),
            cpu_usage=self.process.cpu_percent() - start_data['start_cpu'],
            memory_usage=(self.process.memory_info().rss - start_data['start_memory']) / 1024 / 1024,
            task_count=start_data['task_count']
        )
        self.metrics.append(metrics)
        return metrics
    
    def print_summary(self):
        """Print performance summary"""
        if not self.metrics:
            print("No metrics recorded")
            return
        
        print("\n📊 Performance Summary:")
        print("-" * 50)
        
        for i, metric in enumerate(self.metrics):
            print(f"Run {i+1}:")
            print(f"  Time: {metric.elapsed_time:.2f}s")
            print(f"  Throughput: {metric.throughput:.1f} tasks/sec")
            print(f"  CPU: {metric.cpu_usage:.1f}%")
            print(f"  Memory: {metric.memory_usage:.1f} MB")
            print()

# Usage example
monitor = PerformanceMonitor()

def test_task():
    time.sleep(0.1)
    return "done"

# Test threading performance
start_data = monitor.start_monitoring(10)
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(lambda x: test_task(), range(10)))
metrics = monitor.end_monitoring(start_data)

monitor.print_summary()
```

## 🔧 Optimization Best Practices

### Resource Pool Management

```python
import asyncio
import threading
from contextlib import asynccontextmanager
import queue

class ResourcePool:
    """Generic resource pool for optimization"""
    
    def __init__(self, create_resource, max_size=10):
        self.create_resource = create_resource
        self.pool = queue.Queue(maxsize=max_size)
        self.created_count = 0
        self.max_size = max_size
        self._lock = threading.Lock()
    
    def get_resource(self):
        """Get resource from pool or create new one"""
        try:
            return self.pool.get_nowait()
        except queue.Empty:
            with self._lock:
                if self.created_count < self.max_size:
                    self.created_count += 1
                    return self.create_resource()
                else:
                    # Wait for resource to become available
                    return self.pool.get()
    
    def return_resource(self, resource):
        """Return resource to pool"""
        try:
            self.pool.put_nowait(resource)
        except queue.Full:
            # Pool is full, discard resource
            pass

# Example: HTTP session pool
import requests

def create_session():
    session = requests.Session()
    session.headers.update({'User-Agent': 'MyApp/1.0'})
    return session

session_pool = ResourcePool(create_session, max_size=5)

def optimized_http_request(url):
    """HTTP request using pooled session"""
    session = session_pool.get_resource()
    try:
        response = session.get(url)
        return response.status_code
    finally:
        session_pool.return_resource(session)
```

## 🎯 Performance Tips

### Quick Optimization Checklist

```python
# 1. Use appropriate data structures
from collections import deque, defaultdict
import asyncio

# Good: deque for queue operations
task_queue = deque()
task_queue.append("task1")
first_task = task_queue.popleft()  # O(1)

# 2. Batch operations when possible
async def batch_processor(items, batch_size=100):
    """Process items in batches for better performance"""
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        batch_results = await process_batch(batch)
        results.extend(batch_results)
    return results

# 3. Use connection pooling
async def optimized_http_client():
    connector = aiohttp.TCPConnector(
        limit=100,  # Total connection pool size
        limit_per_host=10,  # Per-host connection limit
        ttl_dns_cache=300,  # DNS cache TTL
        use_dns_cache=True,
    )
    
    timeout = aiohttp.ClientTimeout(total=30, connect=10)
    
    return aiohttp.ClientSession(
        connector=connector,
        timeout=timeout
    )

# 4. Optimize async task creation
async def efficient_task_creation(tasks):
    """Create tasks efficiently"""
    # Bad: Creating tasks one by one
    # for task in tasks:
    #     await asyncio.create_task(task)
    
    # Good: Create all tasks at once
    task_objects = [asyncio.create_task(task) for task in tasks]
    return await asyncio.gather(*task_objects)
```

## 📊 Key Performance Metrics

### What to Measure

1. **Throughput**: Tasks per second
2. **Latency**: Time per task
3. **Resource utilization**: CPU, memory, network
4. **Error rates**: Failed vs successful tasks
5. **Scalability**: Performance under load

### Common Performance Patterns

- **CPU-bound**: Use multiprocessing, cores = workers
- **I/O-bound**: Use asyncio or threading, workers > cores
- **Mixed workload**: Combine approaches (asyncio + ProcessPoolExecutor)
- **High memory**: Use generators and streaming
- **Network-heavy**: Connection pooling and rate limiting

## 🔗 Next Steps

- **Production deployment**: [Production Patterns →](07-production-patterns.md)
- **Debugging issues**: [Debugging Guide →](06-debugging.md)
- **Troubleshooting**: [Troubleshooting →](08-troubleshooting.md) 