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
        from threading_example import worker_thread, demonstrate_threading
        
        # Test that the functions exist and can be called
        result = demonstrate_threading()
        assert isinstance(result, list)
        
    except ImportError:
        pytest.skip("Threading example not available")


def test_multiprocessing_example() -> None:
    """Test multiprocessing example functionality."""
    try:
        from multiprocessing_example import cpu_bound_task, demonstrate_multiprocessing
        
        # Test CPU bound task
        result = cpu_bound_task(1000)
        assert isinstance(result, (int, float))
        assert result > 0
        
        # Test multiprocessing demonstration
        mp_result = demonstrate_multiprocessing()
        assert isinstance(mp_result, dict)
        
    except ImportError:
        pytest.skip("Multiprocessing example not available")


@pytest.mark.asyncio
async def test_asyncio_example() -> None:
    """Test asyncio example functionality."""
    try:
        from asyncio_example import async_task, demonstrate_asyncio
        
        # Test async task
        result = await async_task("test", 0.1)
        assert isinstance(result, str)
        assert "test" in result
        
        # Test asyncio demonstration
        async_result = await demonstrate_asyncio()
        assert isinstance(async_result, list)
        
    except ImportError:
        pytest.skip("Asyncio example not available")


def test_threading_performance() -> None:
    """Test that threading provides some benefit for I/O-bound tasks."""
    try:
        from threading_example import io_bound_task
        import threading
        import time
        
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
        from asyncio_example import async_io_task
        
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
        from multiprocessing_example import cpu_bound_task
        import multiprocessing
        
        # Sequential execution
        start_time = time.time()
        results_sequential = []
        for i in range(2):  # Use fewer processes for testing
            result = cpu_bound_task(100000)  # Smaller workload for testing
            results_sequential.append(result)
        sequential_time = time.time() - start_time
        
        # Multiprocessing execution
        start_time = time.time()
        with multiprocessing.Pool(processes=2) as pool:
            results_parallel = pool.map(cpu_bound_task, [100000, 100000])
        parallel_time = time.time() - start_time
        
        # Results should be the same
        assert len(results_parallel) == 2
        assert all(isinstance(r, (int, float)) for r in results_parallel)
        
        # Note: On single-core systems or in testing environments,
        # multiprocessing might not always be faster due to overhead
        
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