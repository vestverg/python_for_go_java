# Getting Started with Python

This guide will help you get started with Python development, with special focus on differences from Java and Go.

## Installation

### macOS
```bash
brew install python@3.10
```

### Linux
```bash
sudo apt-get update
sudo apt-get install python3.10
```

### Windows
Download the installer from [python.org](https://python.org)

## Package Management Comparison

### Python (pip) vs Go (go mod) vs Java (Maven)

| Feature | Python (pip) | Go (go mod) | Java (Maven) |
|---------|-------------|-------------|--------------|
| Config File | requirements.txt, setup.py | go.mod | pom.xml |
| Lock File | requirements.lock | go.sum | N/A |
| Install Cmd | `pip install` | `go get` | `mvn install` |
| Virtual Env | venv, virtualenv | N/A (built-in) | N/A |
| Version Spec | `package==1.0.0` | `require pkg v1.0.0` | `<version>1.0.0</version>` |

## Your First Python Program

Create a file named `hello.py`:

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(greet("World"))
```

### Comparison with Go

```go
package main

import "fmt"

func greet(name string) string {
    return fmt.Sprintf("Hello, %s!", name)
}

func main() {
    fmt.Println(greet("World"))
}
```

### Comparison with Java

```java
public class Hello {
    public static String greet(String name) {
        return String.format("Hello, %s!", name);
    }

    public static void main(String[] args) {
        System.out.println(greet("World"));
    }
}
```

## Key Differences

1. **Entry Point**
   - Python: `if __name__ == "__main__":`
   - Go: `func main()`
   - Java: `public static void main(String[] args)`

2. **Type Annotations**
   - Python: Optional type hints (`name: str`)
   - Go: Required type declarations
   - Java: Required type declarations

3. **String Formatting**
   - Python: f-strings `f"Hello, {name}!"`
   - Go: `fmt.Sprintf()`
   - Java: `String.format()`

## Next Steps

1. Try running the hello world program
2. Experiment with Python's interactive shell (REPL)
3. Move on to the Basic Syntax section 