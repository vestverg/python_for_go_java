#!/usr/bin/env python3

"""
Example demonstrating Python's multiprocessing capabilities.
"""

import multiprocessing as mp
import time
import random
from typing import List, Tuple
import numpy as np


def cpu_intensive_task(matrix_size: int) -> Tuple[int, float]:
    """
    Perform a CPU-intensive matrix operation.
    
    Args:
        matrix_size: Size of the square matrix
    
    Returns:
        Tuple of process ID and computation time
    """
    # Create random matrices
    matrix_a = np.random.rand(matrix_size, matrix_size)
    matrix_b = np.random.rand(matrix_size, matrix_size)
    
    # Record start time
    start_time = time.time()
    
    # Perform matrix multiplication
    result = np.matmul(matrix_a, matrix_b)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Return process ID and processing time
    return mp.current_process().pid, process_time


def pool_example(matrix_sizes: List[int]) -> None:
    """Example using Pool for parallel processing"""
    print("\nPool Example:")
    print("-------------")
    
    # Create a pool of workers
    with mp.Pool() as pool:
        # Map the task to different matrix sizes
        results = pool.map(cpu_intensive_task, matrix_sizes)
        
        # Print results
        for size, (pid, process_time) in zip(matrix_sizes, results):
            print(f"Process {pid} computed {size}x{size} matrix in {process_time:.2f} seconds")


def process_example(matrix_size: int, result_queue: mp.Queue) -> None:
    """Example using Process with a shared queue"""
    # Perform computation
    pid, process_time = cpu_intensive_task(matrix_size)
    
    # Put result in queue
    result_queue.put((pid, matrix_size, process_time))


def main():
    # Example 1: Using Pool
    matrix_sizes = [100, 200, 300, 400]
    pool_example(matrix_sizes)
    
    print("\nProcess Example:")
    print("---------------")
    
    # Example 2: Using Process with shared queue
    result_queue = mp.Queue()
    
    # Create processes
    processes = [
        mp.Process(
            target=process_example,
            args=(size, result_queue)
        )
        for size in matrix_sizes
    ]
    
    # Start processes
    for p in processes:
        p.start()
    
    # Wait for processes to finish
    for p in processes:
        p.join()
    
    # Get results from queue
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())
    
    # Print results
    for pid, size, process_time in sorted(results, key=lambda x: x[1]):
        print(f"Process {pid} computed {size}x{size} matrix in {process_time:.2f} seconds")


if __name__ == "__main__":
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Run examples
    main() 