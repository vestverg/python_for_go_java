#!/usr/bin/env python3

"""
This example demonstrates Python's functions and methods,
with comparisons to Java and Go concepts.
"""

from typing import List, Dict, Any, Optional, TypeVar, Generic, Callable, Iterator
from dataclasses import dataclass
from functools import wraps
import time


def calculate_total(prices: List[float], tax_rate: float = 0.1, discount: float = 0.0) -> float:
    """Calculates the total price after tax and discount."""
    subtotal = sum(prices)
    subtotal_after_discount = subtotal * (1 - discount)
    total = subtotal_after_discount * (1 + tax_rate)
    return total


def factorial(n: int) -> int:
    """Computes the factorial of a non-negative integer."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def fibonacci_generator(count: int) -> Iterator[int]:
    """Generates the first `count` Fibonacci numbers."""
    a, b = 0, 1
    for _ in range(count):
        yield a
        a, b = b, a + b


def process_with_callback(data: List[Any], callback: Callable[[Any], Any]) -> List[Any]:
    """Processes a list of data using a callback function."""
    return [callback(item) for item in data]


def TimerDecorator(name: str):
    """A decorator that prints the execution time of a function."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"{name}: {end_time - start_time:.4f} seconds")
            return result
        return wrapper
    return decorator


# Type variable for generic types (similar to Java's <T> or Go's interface{})
T = TypeVar('T')


def timing_decorator(func):
    """A decorator that measures function execution time"""
    @wraps(func)  # Preserves function metadata
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper


def retry_decorator(max_attempts: int = 3):
    """A decorator that retries a function on failure"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    print(f"Attempt {attempts} failed, retrying...")
            return None
        return wrapper
    return decorator


@dataclass
class User:
    """User class for demonstration"""
    name: str
    age: int


class Cache(Generic[T]):
    """Generic cache class (similar to Java's generics)"""
    def __init__(self):
        self._data: Dict[str, T] = {}
    
    def get(self, key: str) -> Optional[T]:
        return self._data.get(key)
    
    def set(self, key: str, value: T) -> None:
        self._data[key] = value


def demonstrate_basic_functions():
    """Demonstrate basic function definitions and calls"""
    print("\n=== Basic Functions ===")
    
    # Function with type hints
    def greet(name: str, times: int = 1) -> str:
        """Function with default argument"""
        return f"Hello, {name}!" * times
    
    print(greet("World"))          # Basic call
    print(greet("Python", 3))      # With optional argument
    print(greet(times=2, name="Python"))  # Named arguments


def demonstrate_args_kwargs():
    """Demonstrate variable arguments and keyword arguments"""
    print("\n=== Args and Kwargs ===")
    
    def print_args(*args):
        """Function with variable positional arguments"""
        for i, arg in enumerate(args):
            print(f"Arg {i}: {arg}")
    
    def print_kwargs(**kwargs):
        """Function with variable keyword arguments"""
        for key, value in kwargs.items():
            print(f"{key}: {value}")
    
    print_args(1, "two", 3.0, [4, 5])
    print_kwargs(name="Alice", age=30, city="New York")


def demonstrate_lambda_functions():
    """Demonstrate lambda functions and functional programming"""
    print("\n=== Lambda Functions ===")
    
    # Lambda function
    square = lambda x: x * x
    
    # Using lambda with map and filter
    numbers = [1, 2, 3, 4, 5]
    squared = list(map(square, numbers))
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    
    print(f"Original: {numbers}")
    print(f"Squared: {squared}")
    print(f"Evens: {evens}")
    
    # List comprehension alternatives
    squared_comp = [x * x for x in numbers]
    evens_comp = [x for x in numbers if x % 2 == 0]
    
    print(f"Squared (comprehension): {squared_comp}")
    print(f"Evens (comprehension): {evens_comp}")


@timing_decorator
def slow_function():
    """Function decorated with timing decorator"""
    time.sleep(1)
    return "Done!"


@retry_decorator(max_attempts=3)
def unreliable_function():
    """Function decorated with retry decorator"""
    import random
    if random.random() < 0.7:  # 70% chance of failure
        raise ValueError("Random failure!")
    return "Success!"


class BankAccount:
    """Class demonstrating different method types"""
    
    interest_rate = 0.01  # Class variable
    
    def __init__(self, owner: str, balance: float = 0):
        """Instance method (constructor)"""
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount: float) -> float:
        """Instance method"""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.balance += amount
        return self.balance
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BankAccount':
        """Class method - alternative constructor"""
        return cls(data['owner'], data.get('balance', 0))
    
    @staticmethod
    def validate_amount(amount: float) -> bool:
        """Static method - utility function"""
        return amount > 0
    
    @property
    def balance_display(self) -> str:
        """Property decorator - getter"""
        return f"${self.balance:.2f}"


def main():
    # Demonstrate basic functions
    demonstrate_basic_functions()
    
    # Demonstrate args and kwargs
    demonstrate_args_kwargs()
    
    # Demonstrate lambda functions
    demonstrate_lambda_functions()
    
    # Demonstrate decorators
    print("\n=== Decorators ===")
    print(slow_function())
    try:
        print(unreliable_function())
    except ValueError as e:
        print(f"Final failure: {e}")
    
    # Demonstrate class methods
    print("\n=== Class Methods ===")
    account = BankAccount("Alice", 1000)
    print(f"Initial balance: {account.balance_display}")
    
    account.deposit(500)
    print(f"After deposit: {account.balance_display}")
    
    # Demonstrate class method constructor
    account2 = BankAccount.from_dict({
        'owner': 'Bob',
        'balance': 2000
    })
    print(f"Account 2 balance: {account2.balance_display}")
    
    # Demonstrate generic cache
    print("\n=== Generic Cache ===")
    user_cache: Cache[User] = Cache()
    user_cache.set("alice", User("Alice", 30))
    
    user = user_cache.get("alice")
    if user:
        print(f"Found user: {user.name}, {user.age} years old")


if __name__ == "__main__":
    main() 