# Control Flow in Python

This section covers Python's control flow structures, with comparisons to Java and Go.

## Conditional Statements

### If-Elif-Else

```python
# Python
def check_number(x: int) -> str:
    if x > 0:
        return "positive"
    elif x < 0:
        return "negative"
    else:
        return "zero"
```

```go
// Go
func checkNumber(x int) string {
    if x > 0 {
        return "positive"
    } else if x < 0 {
        return "negative"
    } else {
        return "zero"
    }
}
```

```java
// Java
public String checkNumber(int x) {
    if (x > 0) {
        return "positive";
    } else if (x < 0) {
        return "negative";
    } else {
        return "zero";
    }
}
```

### Match Statement (Python 3.10+)

```python
# Python's match is more powerful than Java's switch or Go's switch
def http_status(code: int) -> str:
    match code:
        case 200 | 201:
            return "Success"
        case 404:
            return "Not Found"
        case 500:
            return "Server Error"
        case _:
            return "Unknown"
```

## Loops

### For Loops

```python
# Python - iterate over sequence
for i in range(5):
    print(i)

# Iterate over list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Enumerate for index and value
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
```

### While Loops

```python
# Python
count = 0
while count < 5:
    print(count)
    count += 1
```

### Loop Control

```python
# Python
for i in range(10):
    if i == 3:
        continue  # Skip to next iteration
    if i == 8:
        break    # Exit loop
    print(i)
```

## Exception Handling

### Basic Try-Except

```python
# Python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
```

### Multiple Exception Types

```python
# Python
try:
    num = int("not a number")
    result = 10 / num
except ValueError:
    print("Invalid number!")
except ZeroDivisionError:
    print("Cannot divide by zero!")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Finally Clause

```python
# Python
try:
    file = open("data.txt")
    # Process file
except FileNotFoundError:
    print("File not found!")
finally:
    file.close()  # Always executed
```

### Context Managers (with statement)

```python
# Python - automatically handles cleanup
with open("data.txt") as file:
    content = file.read()
    # File is automatically closed after this block
```

## Pattern Matching (Python 3.10+)

### Structural Pattern Matching

```python
# Python
def process_command(command: tuple) -> str:
    match command:
        case ("quit",):
            return "Goodbye!"
        case ("greet", name):
            return f"Hello, {name}!"
        case ("move", x, y):
            return f"Moving to ({x}, {y})"
        case _:
            return "Unknown command"
```

### Pattern Matching with Guards

```python
# Python
def process_point(point: tuple) -> str:
    match point:
        case (x, y) if x == y:
            return "On diagonal"
        case (0, y):
            return "On y-axis"
        case (x, 0):
            return "On x-axis"
        case (x, y):
            return f"At point ({x}, {y})"
```

## Next Steps

1. Try the pattern matching examples (requires Python 3.10+)
2. Practice exception handling with real files
3. Experiment with different loop patterns
4. Move on to the Functions section 