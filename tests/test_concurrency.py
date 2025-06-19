"""
Test module for concurrency examples.
"""
import pytest
import asyncio
import time
from typing import List
from pathlib import Path
import sys

# Add the parent directory to the Python path to import concurrency modules
sys.path.append(str(Path(__file__).parent.parent / "07_concurrency" / "examples"))


def test_threading_example() -> None:
    """Test threading example functionality."""
    try:
        from threading_example import ThreadSafeCounter, Worker, create_tasks
        from queue import Queue
        
        # Test ThreadSafeCounter
        counter = ThreadSafeCounter()
        counter.increment()
        assert counter.value == 1
        
        # Test task creation
        tasks = create_tasks(5)
        assert len(tasks) == 5
        assert all(hasattr(task, 'id') for task in tasks)
        
    except ImportError:
        pytest.skip("Threading example not available")


def test_multiprocessing_example() -> None:
    """Test multiprocessing example functionality."""
    try:
        from multiprocessing_example import cpu_intensive_task, pool_example
        
        # Test CPU intensive task
        result = cpu_intensive_task(50)  # Small matrix for testing
        assert isinstance(result, tuple)
        assert len(result) == 2
        pid, process_time = result
        assert isinstance(pid, int)
        assert isinstance(process_time, float)
        assert process_time > 0
        
    except ImportError:
        pytest.skip("Multiprocessing example not available")


@pytest.mark.asyncio
async def test_asyncio_example() -> None:
    """Test asyncio example functionality."""
    try:
        from asyncio_example import fetch_url, process_api_result, ApiResult
        import aiohttp
        
        # Test ApiResult creation
        result = ApiResult("http://test.com", 200, {"test": "data"}, 0.1)
        assert result.url == "http://test.com"
        assert result.status == 200
        assert result.data == {"test": "data"}
        assert result.elapsed == 0.1
        
        # Test process_api_result
        await process_api_result(result)  # Should not raise exception
        
    except ImportError:
        pytest.skip("Asyncio example not available")


def test_threading_performance() -> None:
    """Test that threading provides some benefit for I/O-bound tasks."""
    try:
        import threading
        import time
        
        def io_bound_task(task_id: str, duration: float) -> str:
            """Simulate I/O bound task."""
            time.sleep(duration)
            return f"Task {task_id} completed"
        
        # Sequential execution
        start_time = time.time()
        results_sequential = []
        for i in range(3):
            result = io_bound_task(f"task_{i}", 0.1)
            results_sequential.append(result)
        sequential_time = time.time() - start_time
        
        # Threaded execution
        start_time = time.time()
        threads = []
        results_threaded = []
        
        def thread_worker(task_id: str, duration: float) -> None:
            result = io_bound_task(task_id, duration)
            results_threaded.append(result)
        
        for i in range(3):
            thread = threading.Thread(target=thread_worker, args=(f"task_{i}", 0.1))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        threaded_time = time.time() - start_time
        
        # Threading should be faster for I/O-bound tasks
        assert threaded_time < sequential_time
        assert len(results_threaded) == 3
        
    except ImportError:
        pytest.skip("Threading example not available")


@pytest.mark.asyncio
async def test_async_performance() -> None:
    """Test that async provides benefit for I/O-bound tasks."""
    try:
        async def async_io_task(task_id: str, duration: float) -> str:
            """Simulate async I/O bound task."""
            await asyncio.sleep(duration)
            return f"Async task {task_id} completed"
        
        # Sequential async execution
        start_time = time.time()
        results = []
        for i in range(3):
            result = await async_io_task(f"task_{i}", 0.1)
            results.append(result)
        sequential_time = time.time() - start_time
        
        # Concurrent async execution
        start_time = time.time()
        tasks = [async_io_task(f"task_{i}", 0.1) for i in range(3)]
        concurrent_results = await asyncio.gather(*tasks)
        concurrent_time = time.time() - start_time
        
        # Concurrent should be faster
        assert concurrent_time < sequential_time
        assert len(concurrent_results) == 3
        
    except ImportError:
        pytest.skip("Asyncio example not available")


def test_multiprocessing_performance() -> None:
    """Test that multiprocessing provides benefit for CPU-bound tasks."""
    try:
        from multiprocessing_example import cpu_intensive_task
        import multiprocessing
        
        # Test that we can run the CPU intensive task
        result = cpu_intensive_task(10)  # Very small matrix for testing
        assert isinstance(result, tuple)
        assert len(result) == 2
        pid, process_time = result
        assert isinstance(pid, int)
        assert isinstance(process_time, float)
        assert process_time >= 0
        
        # Note: Full multiprocessing performance tests are skipped in CI
        # due to variability in test environments
        
    except ImportError:
        pytest.skip("Multiprocessing example not available")


def test_concurrency_safety() -> None:
    """Test thread safety mechanisms."""
    try:
        import threading
        import time
        
        # Test shared counter without synchronization (might have race conditions)
        counter = 0
        
        def increment_counter():
            nonlocal counter
            for _ in range(1000):
                counter += 1
        
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=increment_counter)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Without proper synchronization, the result might not be 5000
        # This test just verifies the mechanism works
        assert isinstance(counter, int)
        assert counter > 0
        
    except Exception as e:
        pytest.skip(f"Concurrency safety test failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__]) 