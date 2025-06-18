#!/usr/bin/env python3

"""
This example demonstrates Python's basic data types and operations,
with comparisons to Java and Go concepts.
"""

from typing import List, Dict, Set, Tuple  # Type hints for Java/Go developers


def demonstrate_numbers() -> None:
    # Numbers in Python (no primitive types like in Java)
    integer: int = 42
    float_num: float = 3.14
    complex_num: complex = 1 + 2j
    
    print("\n=== Numbers ===")
    print(f"Integer: {integer}, Type: {type(integer)}")
    print(f"Float: {float_num}, Type: {type(float_num)}")
    print(f"Complex: {complex_num}, Type: {type(complex_num)}")


def demonstrate_strings() -> None:
    # Strings are immutable, like in Java and Go
    text: str = "Hello, World!"
    
    print("\n=== Strings ===")
    print(f"Original: {text}")
    print(f"Upper: {text.upper()}")
    print(f"Lower: {text.lower()}")
    print(f"Split: {text.split(',')}")
    print(f"Replace: {text.replace('World', 'Python')}")
    
    # String formatting (similar to Java's String.format or Go's fmt.Sprintf)
    name = "Python"
    version = 3.9
    print(f"f-string: {name} {version}")  # f-strings (Python 3.6+)
    print("format(): {} {}".format(name, version))  # str.format()
    print("%-format: %s %.1f" % (name, version))  # %-formatting


def demonstrate_lists() -> None:
    # Lists (similar to ArrayList in Java or slices in Go)
    languages: List[str] = ["Python", "Java", "Go"]
    
    print("\n=== Lists ===")
    print(f"Original: {languages}")
    
    # Modifying list
    languages.append("Rust")
    print(f"After append: {languages}")
    
    # Slicing (no direct equivalent in Java/Go)
    print(f"First two: {languages[:2]}")
    print(f"Last two: {languages[-2:]}")
    
    # List comprehension (Python-specific feature)
    lengths: List[int] = [len(lang) for lang in languages]
    print(f"Language lengths: {lengths}")


def demonstrate_tuples() -> None:
    # Tuples (immutable sequences, no direct equivalent in Java/Go)
    point: Tuple[int, int] = (10, 20)
    rgb: Tuple[int, int, int] = (255, 128, 0)
    
    print("\n=== Tuples ===")
    print(f"Point: {point}")
    print(f"RGB Color: {rgb}")
    
    # Tuple unpacking (similar to Go's multiple return values)
    x, y = point
    print(f"Unpacked point: x={x}, y={y}")


def demonstrate_sets() -> None:
    # Sets (similar to HashSet in Java or map[type]struct{} in Go)
    numbers: Set[int] = {1, 2, 3, 2, 1}  # Duplicates are automatically removed
    
    print("\n=== Sets ===")
    print(f"Original set: {numbers}")
    
    # Set operations
    numbers.add(4)
    print(f"After adding 4: {numbers}")
    numbers.remove(1)
    print(f"After removing 1: {numbers}")
    
    # Set operations with another set
    other_numbers: Set[int] = {3, 4, 5}
    print(f"Union: {numbers | other_numbers}")
    print(f"Intersection: {numbers & other_numbers}")


def demonstrate_dictionaries() -> None:
    # Dictionaries (similar to HashMap in Java or map in Go)
    config: Dict[str, any] = {
        "host": "localhost",
        "port": 8080,
        "debug": True
    }
    
    print("\n=== Dictionaries ===")
    print(f"Original: {config}")
    
    # Dictionary operations
    config["timeout"] = 30
    print(f"After adding timeout: {config}")
    
    # Dictionary methods
    print(f"Keys: {list(config.keys())}")
    print(f"Values: {list(config.values())}")
    print(f"Items: {list(config.items())}")
    
    # Get with default (similar to Go's map value, ok syntax)
    print(f"Get port (exists): {config.get('port', 80)}")
    print(f"Get database (doesn't exist): {config.get('database', 'sqlite')}")


def main() -> None:
    demonstrate_numbers()
    demonstrate_strings()
    demonstrate_lists()
    demonstrate_tuples()
    demonstrate_sets()
    demonstrate_dictionaries()


if __name__ == "__main__":
    main() 