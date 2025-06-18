# Functions and Methods in Python

This section covers Python's functions and methods, comparing them with Java and Go equivalents.

## Function Definitions

### Basic Function Definition

```python
# Python
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Call the function
result = greet("World")
```

```java
// Java
public String greet(String name) {
    return "Hello, " + name + "!";
}

// Call the method
String result = greet("World");
```

```go
// Go
func greet(name string) string {
    return fmt.Sprintf("Hello, %s!", name)
}

// Call the function
result := greet("World")
```

### Default Arguments

Python supports default arguments (unlike Go, similar to Java's method overloading):

```python
# Python
def connect(host: str = "localhost", port: int = 8080) -> None:
    print(f"Connecting to {host}:{port}")

# Different ways to call
connect()                    # Uses defaults
connect("example.com")       # Custom host, default port
connect(port=443)           # Named argument, default host
connect("example.com", 443)  # All custom
```

```java
// Java - Method overloading
public void connect() {
    connect("localhost", 8080);
}

public void connect(String host) {
    connect(host, 8080);
}

public void connect(String host, int port) {
    System.out.println("Connecting to " + host + ":" + port);
}
```

```go
// Go - Use struct for optional parameters
type ConnectOptions struct {
    Host string
    Port int
}

func connect(opts ConnectOptions) {
    if opts.Host == "" {
        opts.Host = "localhost"
    }
    if opts.Port == 0 {
        opts.Port = 8080
    }
    fmt.Printf("Connecting to %s:%d\n", opts.Host, opts.Port)
}
```

## Lambda Functions (Anonymous Functions)

```python
# Python
square = lambda x: x * x
numbers = [1, 2, 3]
squared = list(map(lambda x: x * x, numbers))
```

```java
// Java (with lambdas)
Function<Integer, Integer> square = x -> x * x;
List<Integer> squared = numbers.stream()
    .map(x -> x * x)
    .collect(Collectors.toList());
```

```go
// Go
square := func(x int) int { return x * x }
squared := make([]int, len(numbers))
for i, x := range numbers {
    squared[i] = square(x)
}
```

## Args and Kwargs

Python's flexible argument handling:

```python
# Python - Variable positional arguments
def sum_all(*args):
    return sum(args)

result = sum_all(1, 2, 3, 4)  # 10

# Keyword arguments
def config(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

config(host="localhost", port=8080, debug=True)
```

```java
// Java - VarArgs
public int sumAll(int... numbers) {
    return Arrays.stream(numbers).sum();
}

// No direct kwargs equivalent
public void config(Map<String, Object> options) {
    options.forEach((key, value) -> 
        System.out.println(key + ": " + value));
}
```

```go
// Go - Variadic functions
func sumAll(numbers ...int) int {
    sum := 0
    for _, n := range numbers {
        sum += n
    }
    return sum
}

// No direct kwargs equivalent
func config(options map[string]interface{}) {
    for key, value := range options {
        fmt.Printf("%s: %v\n", key, value)
    }
}
```

## Decorators

Python's decorators are similar to Java annotations but more powerful:

```python
# Python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@log_calls
def greet(name):
    return f"Hello, {name}!"
```

```java
// Java
@Logged  // Annotation
public String greet(String name) {
    return "Hello, " + name + "!";
}

// Aspect-oriented programming with Spring
@Around("@annotation(Logged)")
public Object logCalls(ProceedingJoinPoint point) {
    // Implementation
}
```

```go
// Go - Function wrapper pattern
func logCalls(f func(string) string) func(string) string {
    return func(name string) string {
        fmt.Printf("Calling function\n")
        result := f(name)
        fmt.Printf("Finished function\n")
        return result
    }
}

greet := logCalls(func(name string) string {
    return fmt.Sprintf("Hello, %s!", name)
})
```

## Type Hints (Python 3.5+)

Python's type hints are similar to TypeScript for JavaScript:

```python
# Python
from typing import List, Dict, Optional

def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}

def find_user(id: int) -> Optional[User]:
    return db.get_user(id)
```

## Methods in Classes

```python
# Python
class Calculator:
    def __init__(self, initial: int = 0):
        self.value = initial
    
    def add(self, x: int) -> int:
        self.value += x
        return self.value
    
    @classmethod
    def from_string(cls, value: str) -> 'Calculator':
        return cls(int(value))
    
    @staticmethod
    def is_number(value: str) -> bool:
        return value.isdigit()
```

```java
// Java
public class Calculator {
    private int value;
    
    public Calculator(int initial) {
        this.value = initial;
    }
    
    public int add(int x) {
        this.value += x;
        return this.value;
    }
    
    public static Calculator fromString(String value) {
        return new Calculator(Integer.parseInt(value));
    }
    
    public static boolean isNumber(String value) {
        try {
            Integer.parseInt(value);
            return true;
        } catch (NumberFormatException e) {
            return false;
        }
    }
}
```

```go
// Go
type Calculator struct {
    value int
}

func NewCalculator(initial int) *Calculator {
    return &Calculator{value: initial}
}

func (c *Calculator) Add(x int) int {
    c.value += x
    return c.value
}

func NewCalculatorFromString(value string) (*Calculator, error) {
    v, err := strconv.Atoi(value)
    if err != nil {
        return nil, err
    }
    return NewCalculator(v), nil
}

func IsNumber(value string) bool {
    _, err := strconv.Atoi(value)
    return err == nil
}
```

## Exercise: Functions Practice

Create a program that demonstrates:
1. Functions with different parameter types
2. Lambda functions
3. Decorators
4. Type hints
5. Class methods

See the example in the `examples` directory.

## Key Differences from Java/Go

1. **Function Definition**
   - Python: def keyword, optional type hints
   - Java: Access modifiers, strict typing
   - Go: func keyword, strict typing

2. **Default Arguments**
   - Python: Built-in support
   - Java: Method overloading
   - Go: Optional struct parameters

3. **Variable Arguments**
   - Python: *args and **kwargs
   - Java: varargs
   - Go: variadic functions

4. **Decorators/Annotations**
   - Python: Powerful decorator system
   - Java: Annotations with AOP
   - Go: Function wrappers

## Next Steps

Once you're comfortable with Python's functions and methods, move on to the Object-Oriented Programming section, where we'll explore Python's class system and inheritance model. 