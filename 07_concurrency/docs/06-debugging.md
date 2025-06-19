# Debugging and Monitoring

## 🎯 Overview

Debugging concurrent code is challenging. This guide covers essential tools and techniques for identifying concurrency issues.

## 🔍 Common Issues

### Race Conditions

```python
import threading
import time

# Problem: Race condition
shared_counter = 0

def unsafe_increment():
    global shared_counter
    for _ in range(100000):
        shared_counter += 1  # NOT atomic!

# Solution: Use locks
counter_lock = threading.Lock()
safe_counter = 0

def safe_increment():
    global safe_counter
    for _ in range(100000):
        with counter_lock:
            safe_counter += 1
```

### Deadlocks

```python
import threading

# Problem: Deadlock
lock1 = threading.Lock()
lock2 = threading.Lock()

def thread_a():
    with lock1:
        with lock2:  # Different order
            pass

def thread_b():
    with lock2:
        with lock1:  # = deadlock risk
            pass

# Solution: Consistent lock ordering
def safe_thread():
    with lock1:  # Always same order
        with lock2:
            pass
```

## 🛠️ Debugging Tools

### Thread Monitoring

```python
import threading
import time

class ThreadMonitor:
    def __init__(self):
        self.monitoring = False
    
    def start_monitoring(self):
        self.monitoring = True
        monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        monitor_thread.start()
    
    def _monitor_loop(self):
        while self.monitoring:
            threads = threading.enumerate()
            print(f"\n📊 Active threads: {len(threads)}")
            for thread in threads:
                status = "ALIVE" if thread.is_alive() else "DEAD"
                print(f"  {thread.name}: {status}")
            time.sleep(1)
    
    def stop_monitoring(self):
        self.monitoring = False
```

### AsyncIO Debugging

```python
import asyncio
import logging

# Enable debug mode
asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
loop = asyncio.new_event_loop()
loop.set_debug(True)

# Enable warnings
import warnings
warnings.simplefilter('always', ResourceWarning)

# Logging
logging.basicConfig(level=logging.DEBUG)

async def debug_task(name):
    logging.debug(f"Task {name} starting")
    await asyncio.sleep(1)
    logging.debug(f"Task {name} completed")
```

### Lock Profiling

```python
import threading
import time
import collections

class LockProfiler:
    def __init__(self):
        self.lock_stats = collections.defaultdict(lambda: {
            'acquired': 0,
            'contention': 0,
            'wait_time': 0.0
        })
    
    def profile_lock(self, lock, name):
        wait_start = time.time()
        
        # Check contention
        if not lock.acquire(blocking=False):
            self.lock_stats[name]['contention'] += 1
            lock.acquire()  # Now block
        
        wait_time = time.time() - wait_start
        self.lock_stats[name]['acquired'] += 1
        self.lock_stats[name]['wait_time'] += wait_time
        
        return lock
    
    def print_stats(self):
        print("\n🔒 Lock Statistics:")
        for name, stats in self.lock_stats.items():
            print(f"{name}: {stats['acquired']} acquisitions, {stats['contention']} contentions")
```

## 📊 Performance Profiling

### Memory Profiling

```python
import tracemalloc
import threading

class MemoryProfiler:
    def __init__(self):
        self.snapshots = []
    
    def start_tracing(self):
        tracemalloc.start()
        self.take_snapshot("start")
    
    def take_snapshot(self, label):
        if tracemalloc.is_tracing():
            snapshot = tracemalloc.take_snapshot()
            self.snapshots.append((label, snapshot))
    
    def print_diff(self, start_label, end_label):
        start_snap = next((s for l, s in self.snapshots if l == start_label), None)
        end_snap = next((s for l, s in self.snapshots if l == end_label), None)
        
        if start_snap and end_snap:
            top_stats = end_snap.compare_to(start_snap, 'lineno')
            print(f"\n📈 Memory Growth ({start_label} → {end_label}):")
            for stat in top_stats[:5]:
                print(stat)
```

### Timeout Detection

```python
import time
from contextlib import contextmanager

class TimeoutDetector:
    def __init__(self):
        self.timeouts = []
    
    @contextmanager
    def detect_timeout(self, operation, expected_time, tolerance=2.0):
        start = time.time()
        try:
            yield
        finally:
            elapsed = time.time() - start
            if elapsed > expected_time * tolerance:
                print(f"⚠️ Timeout: {operation} took {elapsed:.2f}s (expected {expected_time:.2f}s)")
                self.timeouts.append((operation, elapsed, expected_time))

# Usage
detector = TimeoutDetector()

with detector.detect_timeout("slow_operation", 1.0):
    time.sleep(2)  # Will trigger timeout warning
```

## 🔧 Best Practices

### Structured Logging

```python
import logging
import threading
import json
from datetime import datetime

class ConcurrencyLogger:
    def __init__(self):
        self.logger = logging.getLogger("concurrency")
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_operation(self, operation, **kwargs):
        context = {
            'operation': operation,
            'thread_id': threading.get_ident(),
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        self.logger.info(json.dumps(context))

# Usage
logger = ConcurrencyLogger()

def logged_worker(name):
    logger.log_operation("worker_start", worker_name=name)
    time.sleep(1)
    logger.log_operation("worker_complete", worker_name=name)
```

## 🎯 Quick Diagnostics

### Debug Checklist

1. **Enable Debug Mode**
   ```python
   # AsyncIO
   loop.set_debug(True)
   
   # Enable fault handler
   import faulthandler
   faulthandler.enable()
   ```

2. **Check Resources**
   ```python
   import psutil
   print(f"CPU: {psutil.cpu_percent()}%")
   print(f"Memory: {psutil.virtual_memory().percent}%")
   print(f"Threads: {threading.active_count()}")
   ```

3. **Timeout Locks**
   ```python
   if lock.acquire(timeout=5):
       try:
           # Critical section
           pass
       finally:
           lock.release()
   else:
       print("Lock timeout - possible deadlock")
   ```

4. **Monitor Unawaited Coroutines**
   ```python
   import warnings
   warnings.simplefilter('always', ResourceWarning)
   ```

## 🔗 Next Steps

- **Production patterns**: [Production Patterns →](07-production-patterns.md)
- **Common issues**: [Troubleshooting →](08-troubleshooting.md) 