def greet(name: str) -> str:
    """
    A simple greeting function demonstrating Python syntax.
    
    Args:
        name: The name to greet
        
    Returns:
        A greeting string
    """
    return f"Hello, {name}!"

if __name__ == "__main__":
    # In Python, this block only runs when the file is executed directly
    print(greet("World"))
    
    # Demonstrate Python's dynamic typing (unlike Java/Go)
    print(greet(123))  # This works in Python! The number is converted to string 