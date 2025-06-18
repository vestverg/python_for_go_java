#!/usr/bin/env python3
"""
A simple Hello World program demonstrating Python's basic syntax and type hints.
This example shows key differences from Java and Go.
"""
from typing import List, Optional, Dict, Any


def greet(name: str, times: int = 1) -> str:
    """
    Greets a person multiple times.
    
    Args:
        name: The name of the person to greet
        times: Number of times to repeat the greeting (default: 1)
    
    Returns:
        A greeting string
    
    Example:
        >>> greet("Alice")
        'Hello, Alice!'
        >>> greet("Bob", 2)
        'Hello, Bob!\nHello, Bob!'
    """
    return "\n".join([f"Hello, {name}!" for _ in range(times)])


def process_data(items: List[Any], 
                config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Processes a list of items with optional configuration.
    Demonstrates Python's type hints for collections and optional parameters.
    
    Args:
        items: List of items to process
        config: Optional configuration dictionary
    
    Returns:
        Dictionary containing processed data
    """
    result: Dict[str, Any] = {
        "count": len(items),
        "items": items,
        "has_config": config is not None
    }
    
    if config:
        result.update(config)
    
    return result


def main() -> None:
    # Basic string greeting
    print(greet("World"))
    
    # Multiple greetings
    print("\nMultiple greetings:")
    print(greet("Python", 3))
    
    # Processing data with type hints
    data = process_data(
        items=["apple", "banana", "cherry"],
        config={"sort": True, "filter": None}
    )
    print("\nProcessed data:")
    print(data)


if __name__ == "__main__":
    main() 