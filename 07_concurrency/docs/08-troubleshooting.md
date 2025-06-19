# Troubleshooting Guide

## 🎯 Overview

Common concurrency issues and their solutions.

## 🚫 Threading Issues

### Race Conditions
**Problem:** Inconsistent results, data corruption
```python
# Bad
counter = 0
def unsafe_increment():
    global counter
    counter += 1  # Not atomic!

# Good
lock = threading.Lock()
def safe_increment():
    global counter
    with lock:
        counter += 1
```

### Deadlocks
**Problem:** Application hangs
```python
# Bad: Different lock order
def thread_a():
    with lock1:
        with lock2: pass

def thread_b():
    with lock2:  # Different order!
        with lock1: pass

# Good: Consistent order
def safe_function():
    with lock1:  # Always same order
        with lock2: pass
```

## ⚡ AsyncIO Issues

### Blocking Operations
**Problem:** Event loop blocks
```python
# Bad
async def bad_example():
    time.sleep(1)  # Blocks event loop!

# Good
async def good_example():
    await asyncio.sleep(1)  # Non-blocking
```

### Unawaited Coroutines
**Problem:** ResourceWarning, tasks not executing
```python
# Bad
async def problem():
    fetch_data()  # Not awaited!

# Good
async def solution():
    result = await fetch_data()
    return result
```

## 🔄 Multiprocessing Issues

### Pickle Errors
**Problem:** "TypeError: can't pickle"
```python
# Bad
# pool.map(lambda x: x * 2, data)  # Can't pickle lambda

# Good
def double(x):
    return x * 2

pool.map(double, data)
```

### Platform Issues
**Problem:** Different behavior on Windows/Linux
```python
import sys
import multiprocessing as mp

if __name__ == "__main__":
    if sys.platform == "win32":
        mp.set_start_method("spawn")
    
    # Your code here
```

## 📊 Performance Issues

### Poor Scalability
**Solution:** Profile and optimize worker counts
```python
def find_optimal_workers():
    for workers in [1, 2, 4, 8]:
        start = time.time()
        with ThreadPoolExecutor(max_workers=workers) as executor:
            # Your tasks
            pass
        print(f"Workers: {workers}, Time: {time.time() - start:.2f}s")
```

### Memory Leaks
**Solution:** Monitor and fix resource management
```python
import tracemalloc

tracemalloc.start()
# Your code
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
```

## 🛠️ Quick Fixes

### Enable Debugging
```python
# AsyncIO debug mode
asyncio.get_event_loop().set_debug(True)

# Resource warnings
import warnings
warnings.simplefilter('always', ResourceWarning)
```

### Use Timeouts
```python
# AsyncIO
async with asyncio.timeout(5.0):
    await operation()

# Threading
if lock.acquire(timeout=5.0):
    try:
        # Critical section
        pass
    finally:
        lock.release()
```

### Monitor Resources
```python
import psutil

process = psutil.Process()
print(f"CPU: {process.cpu_percent()}%")
print(f"Memory: {process.memory_info().rss/1024/1024:.1f}MB")
print(f"Threads: {threading.active_count()}")
```

## 📋 Diagnostic Checklist

**Threading:**
- [ ] Shared variables protected by locks?
- [ ] Consistent lock ordering?
- [ ] Using ThreadPoolExecutor?

**AsyncIO:**
- [ ] All coroutines awaited?
- [ ] No blocking operations?
- [ ] Tasks properly cancelled?

**Multiprocessing:**
- [ ] Functions pickle-able?
- [ ] Using `if __name__ == "__main__"`?
- [ ] Processes properly managed?

## 🔗 Next Steps

- [Production Patterns →](07-production-patterns.md)
- [Performance Guide →](05-performance.md)
- [Debugging Guide →](06-debugging.md) 