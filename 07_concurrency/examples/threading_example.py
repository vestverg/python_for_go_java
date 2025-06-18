#!/usr/bin/env python3

"""
Example demonstrating Python's threading capabilities.
"""

import threading
import time
import random
from queue import Queue
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Task:
    """Represents a task to be processed"""
    id: int
    data: str
    result: Optional[str] = None


class ThreadSafeCounter:
    """Thread-safe counter implementation"""
    
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()
    
    def increment(self) -> None:
        with self._lock:
            self._value += 1
    
    @property
    def value(self) -> int:
        return self._value


class Worker(threading.Thread):
    """Worker thread that processes tasks"""
    
    def __init__(self, name: str, task_queue: Queue, counter: ThreadSafeCounter):
        super().__init__(name=name)
        self.task_queue = task_queue
        self.counter = counter
        self.running = True
    
    def run(self) -> None:
        """Main worker loop"""
        while self.running:
            try:
                # Get task with timeout
                task = self.task_queue.get(timeout=1.0)
                
                # Process task
                self._process_task(task)
                
                # Mark task as done
                self.task_queue.task_done()
                
                # Update counter
                self.counter.increment()
                
            except Queue.Empty:
                # No more tasks
                continue
    
    def _process_task(self, task: Task) -> None:
        """Process a single task"""
        print(f"{self.name} processing Task {task.id}")
        
        # Simulate work
        time.sleep(random.uniform(0.1, 0.5))
        
        # Set result
        task.result = f"Processed {task.data} by {self.name}"
    
    def stop(self) -> None:
        """Stop the worker"""
        self.running = False


def create_tasks(count: int) -> List[Task]:
    """Create a list of tasks"""
    return [
        Task(id=i, data=f"Data-{i}")
        for i in range(count)
    ]


def main():
    # Create shared objects
    task_queue: Queue = Queue()
    counter = ThreadSafeCounter()
    
    # Create tasks
    tasks = create_tasks(10)
    for task in tasks:
        task_queue.put(task)
    
    # Create workers
    workers = [
        Worker(f"Worker-{i}", task_queue, counter)
        for i in range(3)
    ]
    
    print("Starting workers...")
    
    # Start workers
    for worker in workers:
        worker.start()
    
    # Wait for all tasks to be processed
    task_queue.join()
    
    print("\nStopping workers...")
    
    # Stop workers
    for worker in workers:
        worker.stop()
    
    # Wait for workers to finish
    for worker in workers:
        worker.join()
    
    print(f"\nProcessed {counter.value} tasks")
    print("\nResults:")
    for task in tasks:
        print(f"Task {task.id}: {task.result}")


if __name__ == "__main__":
    main() 