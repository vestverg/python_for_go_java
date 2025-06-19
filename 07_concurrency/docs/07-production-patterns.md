# Production Patterns

## 🎯 Overview

This guide covers production-ready patterns for deploying concurrent Python applications at scale.

## 🌐 Web Server Patterns

### High-Performance AsyncIO Server

```python
import asyncio
import aiohttp
from aiohttp import web
import logging
import signal
import os

class ProductionServer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.app = web.Application()
        self.setup_routes()
        self.setup_middleware()
    
    def setup_routes(self):
        self.app.router.add_get('/health', self.health_check)
        self.app.router.add_get('/api/data', self.get_data)
        self.app.router.add_post('/api/process', self.process_data)
    
    def setup_middleware(self):
        @web.middleware
        async def error_middleware(request, handler):
            try:
                return await handler(request)
            except Exception as e:
                logging.error(f"Request error: {e}")
                return web.json_response(
                    {'error': 'Internal server error'}, 
                    status=500
                )
        
        self.app.middlewares.append(error_middleware)
    
    async def health_check(self, request):
        return web.json_response({'status': 'healthy'})
    
    async def get_data(self, request):
        # Simulate async database query
        await asyncio.sleep(0.1)
        return web.json_response({'data': 'sample data'})
    
    async def process_data(self, request):
        data = await request.json()
        # Process data asynchronously
        result = await self.process_async(data)
        return web.json_response({'result': result})
    
    async def process_async(self, data):
        # Simulate async processing
        await asyncio.sleep(0.5)
        return f"Processed: {data}"
    
    async def start_server(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        
        print(f"Server running on {self.host}:{self.port}")
        return runner

# Production deployment
async def main():
    server = ProductionServer()
    runner = await server.start_server()
    
    # Graceful shutdown
    def signal_handler():
        print("Shutting down server...")
        asyncio.create_task(runner.cleanup())
    
    # Register signal handlers
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, lambda s, f: signal_handler())
    
    # Keep server running
    try:
        await asyncio.Future()  # Run forever
    except KeyboardInterrupt:
        await runner.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

### Worker Pool Architecture

```python
import multiprocessing as mp
import queue
import time
import logging
from typing import Any, Callable

class WorkerPool:
    def __init__(self, num_workers=None, max_queue_size=1000):
        self.num_workers = num_workers or mp.cpu_count()
        self.task_queue = mp.Queue(maxsize=max_queue_size)
        self.result_queue = mp.Queue()
        self.workers = []
        self.running = False
    
    def start(self):
        """Start the worker pool"""
        self.running = True
        
        for i in range(self.num_workers):
            worker = mp.Process(
                target=self._worker_loop,
                args=(i, self.task_queue, self.result_queue)
            )
            worker.start()
            self.workers.append(worker)
        
        logging.info(f"Started {self.num_workers} workers")
    
    def _worker_loop(self, worker_id, task_queue, result_queue):
        """Main worker loop"""
        while True:
            try:
                task = task_queue.get(timeout=1)
                if task is None:  # Shutdown signal
                    break
                
                func, args, kwargs, task_id = task
                try:
                    result = func(*args, **kwargs)
                    result_queue.put((task_id, result, None))
                except Exception as e:
                    result_queue.put((task_id, None, str(e)))
                
            except queue.Empty:
                continue
    
    def submit_task(self, func: Callable, *args, **kwargs) -> str:
        """Submit task to worker pool"""
        task_id = f"task_{time.time()}_{id(func)}"
        task = (func, args, kwargs, task_id)
        
        try:
            self.task_queue.put(task, timeout=5)
            return task_id
        except queue.Full:
            raise RuntimeError("Task queue is full")
    
    def get_result(self, timeout=None):
        """Get result from worker"""
        try:
            return self.result_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def shutdown(self):
        """Gracefully shutdown worker pool"""
        self.running = False
        
        # Send shutdown signal to all workers
        for _ in self.workers:
            self.task_queue.put(None)
        
        # Wait for workers to finish
        for worker in self.workers:
            worker.join(timeout=5)
            if worker.is_alive():
                worker.terminate()
        
        logging.info("Worker pool shut down")

# Usage example
def cpu_intensive_task(data):
    """Example CPU-intensive task"""
    total = 0
    for i in range(1000000):
        total += i * len(str(data))
    return total

# Production usage
if __name__ == "__main__":
    pool = WorkerPool(num_workers=4)
    pool.start()
    
    try:
        # Submit tasks
        task_ids = []
        for i in range(10):
            task_id = pool.submit_task(cpu_intensive_task, f"data_{i}")
            task_ids.append(task_id)
        
        # Collect results
        results = {}
        for _ in range(10):
            result = pool.get_result(timeout=30)
            if result:
                task_id, value, error = result
                results[task_id] = (value, error)
        
        print(f"Processed {len(results)} tasks")
        
    finally:
        pool.shutdown()
```

## 📋 Task Queue Systems

### Redis-Based Task Queue

```python
import asyncio
import json
import redis.asyncio as redis
import logging
from typing import Dict, Any
import uuid

class AsyncTaskQueue:
    def __init__(self, redis_url="redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self.queue_name = "task_queue"
        self.result_prefix = "result:"
        self.running = False
    
    async def enqueue_task(self, task_type: str, data: Dict[str, Any]) -> str:
        """Enqueue a task for processing"""
        task_id = str(uuid.uuid4())
        task = {
            'id': task_id,
            'type': task_type,
            'data': data,
            'created_at': asyncio.get_event_loop().time()
        }
        
        await self.redis.lpush(self.queue_name, json.dumps(task))
        logging.info(f"Enqueued task {task_id} of type {task_type}")
        return task_id
    
    async def dequeue_task(self, timeout=10):
        """Dequeue a task for processing"""
        result = await self.redis.brpop(self.queue_name, timeout=timeout)
        if result:
            _, task_data = result
            return json.loads(task_data)
        return None
    
    async def store_result(self, task_id: str, result: Any, ttl=3600):
        """Store task result"""
        key = f"{self.result_prefix}{task_id}"
        await self.redis.setex(key, ttl, json.dumps(result))
    
    async def get_result(self, task_id: str):
        """Get task result"""
        key = f"{self.result_prefix}{task_id}"
        result = await self.redis.get(key)
        return json.loads(result) if result else None
    
    async def worker_loop(self, worker_id: str):
        """Main worker loop"""
        logging.info(f"Worker {worker_id} started")
        
        while self.running:
            try:
                task = await self.dequeue_task(timeout=1)
                if task:
                    await self.process_task(worker_id, task)
            except Exception as e:
                logging.error(f"Worker {worker_id} error: {e}")
                await asyncio.sleep(1)
    
    async def process_task(self, worker_id: str, task: Dict):
        """Process a single task"""
        task_id = task['id']
        task_type = task['type']
        data = task['data']
        
        logging.info(f"Worker {worker_id} processing task {task_id}")
        
        try:
            # Route task to appropriate handler
            if task_type == "email":
                result = await self.send_email(data)
            elif task_type == "report":
                result = await self.generate_report(data)
            else:
                raise ValueError(f"Unknown task type: {task_type}")
            
            await self.store_result(task_id, {
                'success': True,
                'result': result,
                'processed_by': worker_id
            })
            
        except Exception as e:
            logging.error(f"Task {task_id} failed: {e}")
            await self.store_result(task_id, {
                'success': False,
                'error': str(e),
                'processed_by': worker_id
            })
    
    async def send_email(self, data):
        """Mock email sending"""
        await asyncio.sleep(1)  # Simulate email service delay
        return f"Email sent to {data.get('recipient')}"
    
    async def generate_report(self, data):
        """Mock report generation"""
        await asyncio.sleep(2)  # Simulate report generation
        return f"Report generated for {data.get('type')}"
    
    async def start_workers(self, num_workers=3):
        """Start worker processes"""
        self.running = True
        
        workers = []
        for i in range(num_workers):
            worker_id = f"worker_{i}"
            worker = asyncio.create_task(self.worker_loop(worker_id))
            workers.append(worker)
        
        return workers
    
    def stop_workers(self):
        """Stop all workers"""
        self.running = False

# Usage example
async def main():
    queue = AsyncTaskQueue()
    
    # Start workers
    workers = await queue.start_workers(num_workers=3)
    
    try:
        # Enqueue some tasks
        email_task = await queue.enqueue_task("email", {
            "recipient": "user@example.com",
            "subject": "Test Email"
        })
        
        report_task = await queue.enqueue_task("report", {
            "type": "monthly",
            "user_id": 123
        })
        
        # Wait for processing
        await asyncio.sleep(5)
        
        # Check results
        email_result = await queue.get_result(email_task)
        report_result = await queue.get_result(report_task)
        
        print(f"Email result: {email_result}")
        print(f"Report result: {report_result}")
        
    finally:
        queue.stop_workers()
        await asyncio.gather(*workers, return_exceptions=True)

if __name__ == "__main__":
    asyncio.run(main())
```

## 🔄 Circuit Breaker Pattern

```python
import asyncio
import time
from enum import Enum
from typing import Callable, Any
import logging

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, 
                 failure_threshold=5,
                 recovery_timeout=60,
                 success_threshold=2):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection"""
        
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                logging.info("Circuit breaker: HALF_OPEN")
            else:
                raise CircuitOpenError("Circuit breaker is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
            
        except Exception as e:
            self._on_failure()
            raise e
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        if self.last_failure_time is None:
            return True
        
        return (time.time() - self.last_failure_time) >= self.recovery_timeout
    
    def _on_success(self):
        """Handle successful call"""
        self.failure_count = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0
                logging.info("Circuit breaker: CLOSED")
    
    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        self.success_count = 0
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logging.info("Circuit breaker: OPEN")

class CircuitOpenError(Exception):
    """Raised when circuit breaker is open"""
    pass

# Usage example
async def unreliable_service():
    """Simulate unreliable external service"""
    if time.time() % 10 < 3:  # Fail 30% of the time
        raise ConnectionError("Service unavailable")
    
    await asyncio.sleep(0.1)
    return "Service response"

async def test_circuit_breaker():
    breaker = CircuitBreaker(
        failure_threshold=3,
        recovery_timeout=5,
        success_threshold=2
    )
    
    for i in range(20):
        try:
            result = await breaker.call(unreliable_service)
            print(f"Call {i}: {result} (State: {breaker.state.value})")
        except Exception as e:
            print(f"Call {i}: Failed - {e} (State: {breaker.state.value})")
        
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(test_circuit_breaker())
```

## 📊 Monitoring and Metrics

### Application Metrics

```python
import asyncio
import time
import threading
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Dict, List
import json

@dataclass
class Metric:
    name: str
    value: float
    timestamp: float
    tags: Dict[str, str] = None

class MetricsCollector:
    def __init__(self, max_history=1000):
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_history))
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = defaultdict(float)
        self._lock = threading.Lock()
    
    def increment(self, name: str, value: int = 1, tags: Dict = None):
        """Increment a counter metric"""
        with self._lock:
            self.counters[name] += value
            self._record_metric(name, self.counters[name], tags)
    
    def gauge(self, name: str, value: float, tags: Dict = None):
        """Set a gauge metric"""
        with self._lock:
            self.gauges[name] = value
            self._record_metric(name, value, tags)
    
    def timing(self, name: str, duration: float, tags: Dict = None):
        """Record a timing metric"""
        with self._lock:
            self._record_metric(name, duration, tags)
    
    def _record_metric(self, name: str, value: float, tags: Dict = None):
        """Record metric in history"""
        metric = Metric(
            name=name,
            value=value,
            timestamp=time.time(),
            tags=tags or {}
        )
        self.metrics[name].append(metric)
    
    def get_metrics_summary(self) -> Dict:
        """Get summary of all metrics"""
        with self._lock:
            summary = {
                'counters': dict(self.counters),
                'gauges': dict(self.gauges),
                'timestamp': time.time()
            }
            
            # Add averages for timing metrics
            timing_metrics = {}
            for name, history in self.metrics.items():
                if name.endswith('_time') or name.endswith('_duration'):
                    recent_values = [m.value for m in list(history)[-100:]]
                    if recent_values:
                        timing_metrics[f"{name}_avg"] = sum(recent_values) / len(recent_values)
            
            summary['timings'] = timing_metrics
            return summary

# Timing decorator
def track_timing(metrics: MetricsCollector, metric_name: str):
    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            async def async_wrapper(*args, **kwargs):
                start = time.time()
                try:
                    result = await func(*args, **kwargs)
                    metrics.increment(f"{metric_name}_success")
                    return result
                except Exception as e:
                    metrics.increment(f"{metric_name}_error")
                    raise
                finally:
                    duration = time.time() - start
                    metrics.timing(f"{metric_name}_duration", duration)
            return async_wrapper
        else:
            def sync_wrapper(*args, **kwargs):
                start = time.time()
                try:
                    result = func(*args, **kwargs)
                    metrics.increment(f"{metric_name}_success")
                    return result
                except Exception as e:
                    metrics.increment(f"{metric_name}_error")
                    raise
                finally:
                    duration = time.time() - start
                    metrics.timing(f"{metric_name}_duration", duration)
            return sync_wrapper
    return decorator

# Usage example
metrics = MetricsCollector()

@track_timing(metrics, "api_call")
async def api_call(endpoint: str):
    """Simulated API call"""
    await asyncio.sleep(0.1)  # Simulate network delay
    
    if endpoint == "/error":
        raise ValueError("API Error")
    
    return {"status": "success", "endpoint": endpoint}

async def metrics_example():
    """Example of using metrics in production"""
    
    # Start metrics reporting task
    async def report_metrics():
        while True:
            await asyncio.sleep(10)
            summary = metrics.get_metrics_summary()
            print(f"Metrics: {json.dumps(summary, indent=2)}")
    
    reporting_task = asyncio.create_task(report_metrics())
    
    try:
        # Simulate API calls
        for i in range(50):
            endpoint = "/error" if i % 10 == 0 else f"/api/endpoint{i%3}"
            
            try:
                await api_call(endpoint)
                metrics.increment("requests_total", tags={"endpoint": endpoint})
            except Exception:
                metrics.increment("requests_total", tags={"endpoint": endpoint, "status": "error"})
            
            # Update gauge metrics
            metrics.gauge("active_connections", i % 20)
            
            await asyncio.sleep(0.1)
    
    finally:
        reporting_task.cancel()

if __name__ == "__main__":
    asyncio.run(metrics_example())
```

## 🔧 Configuration Management

### Environment-Based Config

```python
import os
import json
from dataclasses import dataclass
from typing import Optional

@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    database: str = "myapp"
    username: str = "user"
    password: str = "password"
    pool_size: int = 10

@dataclass
class RedisConfig:
    host: str = "localhost"
    port: int = 6379
    database: int = 0
    password: Optional[str] = None

@dataclass
class ServerConfig:
    host: str = "0.0.0.0"
    port: int = 8080
    workers: int = 4
    debug: bool = False

@dataclass
class AppConfig:
    database: DatabaseConfig
    redis: RedisConfig
    server: ServerConfig
    log_level: str = "INFO"

def load_config() -> AppConfig:
    """Load configuration from environment variables"""
    
    # Database config
    db_config = DatabaseConfig(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME", "myapp"),
        username=os.getenv("DB_USER", "user"),
        password=os.getenv("DB_PASSWORD", "password"),
        pool_size=int(os.getenv("DB_POOL_SIZE", "10"))
    )
    
    # Redis config
    redis_config = RedisConfig(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", "6379")),
        database=int(os.getenv("REDIS_DB", "0")),
        password=os.getenv("REDIS_PASSWORD")
    )
    
    # Server config
    server_config = ServerConfig(
        host=os.getenv("SERVER_HOST", "0.0.0.0"),
        port=int(os.getenv("SERVER_PORT", "8080")),
        workers=int(os.getenv("SERVER_WORKERS", "4")),
        debug=os.getenv("DEBUG", "false").lower() == "true"
    )
    
    return AppConfig(
        database=db_config,
        redis=redis_config,
        server=server_config,
        log_level=os.getenv("LOG_LEVEL", "INFO")
    )

# Usage
config = load_config()
print(f"Server will run on {config.server.host}:{config.server.port}")
print(f"Database: {config.database.host}:{config.database.port}/{config.database.database}")
```

## 🔗 Next Steps

- **Debugging issues**: [Debugging Guide →](06-debugging.md)
- **Common problems**: [Troubleshooting →](08-troubleshooting.md)
- **Performance tuning**: [Performance Guide →](05-performance.md) 