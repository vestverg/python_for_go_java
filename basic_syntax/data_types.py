from typing import List, Dict, Optional, Tuple

def demonstrate_numbers() -> None:
    """Demonstrate Python's number types."""
    # Integer operations
    x: int = 42
    y: int = 10
    print(f"Integer division: {x // y}")  # Floor division
    print(f"True division: {x / y}")      # Float division
    print(f"Modulo: {x % y}")            # Remainder
    
    # Float operations
    pi: float = 3.14159
    print(f"Rounded: {round(pi, 2)}")
    
    # Complex numbers
    c: complex = 1 + 2j
    print(f"Complex number: {c}")
    print(f"Real part: {c.real}, Imaginary part: {c.imag}")

def demonstrate_strings() -> None:
    """Demonstrate string operations."""
    # String creation
    single: str = 'Single quotes'
    double: str = "Double quotes"
    multi: str = """
    Multi-line
    string
    """
    
    # String operations
    text: str = "Hello, World!"
    print(f"Upper: {text.upper()}")
    print(f"Lower: {text.lower()}")
    print(f"Split: {text.split(',')}")
    print(f"Replace: {text.replace('Hello', 'Hi')}")
    
    # String formatting
    name: str = "Alice"
    age: int = 30
    print(f"Format: {name} is {age} years old")
    print("Format: {} is {} years old".format(name, age))  # older style

def demonstrate_lists() -> List[int]:
    """Demonstrate list operations."""
    # List creation and basic operations
    numbers: List[int] = [1, 2, 3, 4, 5]
    numbers.append(6)
    numbers.extend([7, 8])
    
    # List slicing
    print(f"First two: {numbers[:2]}")
    print(f"Last two: {numbers[-2:]}")
    print(f"Every second: {numbers[::2]}")
    
    # List comprehension
    squares: List[int] = [x * x for x in numbers]
    evens: List[int] = [x for x in numbers if x % 2 == 0]
    
    return evens

def demonstrate_dict() -> Dict[str, any]:
    """Demonstrate dictionary operations."""
    # Dictionary creation
    person: Dict[str, any] = {
        "name": "Bob",
        "age": 25,
        "languages": ["Python", "Go", "Java"]
    }
    
    # Dictionary operations
    person["email"] = "bob@example.com"  # Add new key
    age: Optional[int] = person.get("age")  # Safe get
    
    # Dictionary comprehension
    squares: Dict[int, int] = {x: x*x for x in range(5)}
    
    return squares

def demonstrate_tuple_operations() -> Tuple[int, int]:
    """Demonstrate tuple operations."""
    # Tuple creation
    point: Tuple[int, int] = (3, 4)
    
    # Tuple unpacking
    x, y = point
    
    # Tuples are immutable
    try:
        point[0] = 5  # This will raise an error
    except TypeError as e:
        print(f"Error: {e}")
    
    return point

if __name__ == "__main__":
    print("=== Numbers ===")
    demonstrate_numbers()
    
    print("\n=== Strings ===")
    demonstrate_strings()
    
    print("\n=== Lists ===")
    evens = demonstrate_lists()
    print(f"Even numbers: {evens}")
    
    print("\n=== Dictionaries ===")
    squares = demonstrate_dict()
    print(f"Squares: {squares}")
    
    print("\n=== Tuples ===")
    point = demonstrate_tuple_operations()
    print(f"Point: {point}") 