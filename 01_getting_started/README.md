# 🚀 Getting Started with Python for Java and Go Developers

## 📖 Introduction

This section serves as your entry point into Python development, specifically tailored for developers with Java or Go experience. We'll cover the fundamental differences in development environments, tooling, and basic syntax patterns.

## 💻 Development Environment Setup

### 🐍 Python Installation

Unlike Java's JDK or Go's SDK, Python's installation is straightforward but requires attention to version management:

```bash
# Check Python version
python --version  # Should be 3.10+

# Check pip version
pip --version
```

#### 🔧 Version Management Tools
- **pyenv** (similar to Java's jenv or Go's gvm)
  ```bash
  # Install pyenv (macOS)
  brew install pyenv
  
  # Install specific Python version
  pyenv install 3.10.0
  ```

### 🔮 Virtual Environments

Virtual environments in Python serve a similar purpose to Java's Maven/Gradle scopes or Go's module system:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Unix/macOS
.\venv\Scripts\activate   # Windows

# Deactivate when done
deactivate
```

## 📦 Package Management

### 🔄 Comparison with Java and Go

| Feature | Python (pip) | Java (Maven) | Go (modules) |
|---------|-------------|--------------|--------------|
| Package Definition | requirements.txt | pom.xml | go.mod |
| Lock File | requirements.lock | pom.xml | go.sum |
| Install Command | pip install | mvn install | go get |
| Project Structure | Flexible | Standardized | Go Workspace |
| Version Constraint | ~=1.2.3 | 1.2.3 | v1.2.3 |

### 💡 Common Commands

```bash
# Install packages
pip install -r requirements.txt

# Add new package
pip install requests
pip freeze > requirements.txt

# Development dependencies
pip install -r requirements-dev.txt
```

## 🛠️ IDE Support

### 🌟 Popular IDEs and Their Features

1. **🔷 PyCharm** (Similar to IntelliJ IDEA)
   - Full Python support
   - Integrated debugger
   - Virtual environment management
   - Type hint support

2. **🆚 VS Code with Python Extension**
   - Lightweight
   - Multi-language support
   - Integrated terminal
   - Debugging support

3. **📓 Jupyter Notebooks**
   - Interactive development
   - Rich output display
   - Markdown documentation
   - Code and documentation mixing

## 🏷️ Type System Introduction

### 🔄 Static vs Dynamic Typing

Python's type system differs significantly from Java and Go:

```python
# Python - Dynamic with optional type hints
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Java equivalent
public String greet(String name) {
    return "Hello, " + name + "!";
}

# Go equivalent
func greet(name string) string {
    return fmt.Sprintf("Hello, %s!", name)
}
```

### 🔍 Type Checking Tools

1. **🔎 mypy** - Static Type Checker
   ```bash
   # Install mypy
   pip install mypy
   
   # Run type checking
   mypy your_file.py
   ```

2. **🔧 pylint** - Linter with Type Checking
   ```bash
   # Install pylint
   pip install pylint
   
   # Run linting
   pylint your_file.py
   ```

## 📁 Project Structure

### 📂 Standard Python Project Layout
```
project_root/
├── src/
│   └── package/
│       ├── __init__.py
│       └── module.py
├── tests/
│   └── test_module.py
├── docs/
├── requirements.txt
├── setup.py
└── README.md
```

### ⚙️ Configuration Files

1. **📋 setup.py** (Similar to pom.xml or go.mod)
   - Package metadata
   - Dependencies
   - Build configuration

2. **📄 requirements.txt**
   - Direct dependencies
   - Version constraints
   - Development tools

3. **🔧 pyproject.toml**
   - Build system requirements
   - Tool configuration
   - Development dependencies

## ⭐ Best Practices

### 🎨 Code Style

1. **📐 PEP 8** - Python Style Guide
   - 4 spaces for indentation
   - Maximum line length of 79 characters
   - Snake case for functions and variables
   - Pascal case for classes

2. **🏷️ Type Hints**
   - Use for function parameters
   - Use for return types
   - Use for complex data structures
   - Document nullable types

3. **📝 Documentation**
   - Docstrings for modules, classes, and functions
   - Type information in docstrings
   - Usage examples in docstrings
   - README files for packages

### 🧪 Testing

1. **🔬 pytest** Framework
   ```python
   # test_example.py
   def test_greet():
       assert greet("World") == "Hello, World!"
   ```

2. **▶️ Test Running**
   ```bash
   # Run tests
   pytest
   
   # Run with coverage
   pytest --cov=.
   ```

## ⚠️ Common Gotchas for Java/Go Developers

1. **📏 Indentation Matters**
   - Python uses indentation for blocks
   - No curly braces or semicolons
   - Consistent indentation required

2. **🎯 Everything is an Object**
   - No primitives like in Java
   - Methods on all types
   - Duck typing vs static typing

3. **📦 Package Management**
   - Virtual environments vs classpath
   - pip vs Maven/Gradle
   - requirements.txt vs pom.xml/go.mod

4. **🚨 Error Handling**
   - Exceptions vs checked exceptions
   - try/except vs try/catch
   - Context managers vs try-with-resources

## 🎯 Next Steps

1. Explore the `hello.py` example
2. Run the test suite
3. Try modifying the code
4. Experiment with type hints
5. Move on to Basic Syntax section

## 📚 Additional Resources

1. **📖 Official Documentation**
   - [Python Documentation](https://docs.python.org/3/)
   - [PEP 484 - Type Hints](https://www.python.org/dev/peps/pep-0484/)
   - [PEP 8 - Style Guide](https://www.python.org/dev/peps/pep-0008/)

2. **🛠️ Tools Documentation**
   - [mypy Documentation](http://mypy-lang.org/)
   - [pytest Documentation](https://docs.pytest.org/)
   - [pip Documentation](https://pip.pypa.io/)

## 🐍 Python Installation

### 💻 System Requirements
- Python 3.8 or higher (3.10+ recommended for latest features)
- pip (Python package installer)
- Virtual environment support

### 🖥️ Installation by Platform

#### 🍎 macOS
```bash
# Using Homebrew (recommended)
brew install python

# Using pyenv for multiple Python versions
brew install pyenv
pyenv install 3.11.0
pyenv global 3.11.0

# Verify installation
python3 --version
pip3 --version
```

#### 🐧 Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Install additional development tools
sudo apt install python3-dev build-essential

# Verify installation
python3 --version
pip3 --version
```

#### 🪟 Windows
```powershell
# Download from python.org and install
# Or use Windows Package Manager
winget install Python.Python.3.11

# Or use Chocolatey
choco install python

# Verify installation (use 'py' launcher)
py --version
py -m pip --version
```

## 🔮 Virtual Environments

Virtual environments are **essential** for Python development. They provide isolated Python environments for different projects, preventing dependency conflicts.

### ❓ Why Virtual Environments?

Unlike Java's classpath or Go's modules, Python has a global site-packages directory. Virtual environments solve:

- **⚔️ Dependency Conflicts**: Different projects requiring different versions of the same package
- **🛡️ System Pollution**: Avoiding modifications to system Python
- **🔄 Reproducible Environments**: Ensuring consistent dependencies across development/production
- **🔐 Permission Issues**: Installing packages without root/administrator privileges

### 📊 Comparison with Java and Go

| Aspect | Python (venv) | Java | Go |
|--------|---------------|------|-----|
| **🔒 Isolation** | Virtual environments | JAR files, Maven/Gradle | Go modules |
| **📦 Dependency Management** | pip + requirements.txt | Maven pom.xml, Gradle | go.mod, go.sum |
| **🔄 Version Management** | pyenv, conda | SDKMAN, jenv | Go toolchain |
| **📁 Project Structure** | Virtual env + project | Maven/Gradle structure | Module-based |

### 🛠️ Using venv (Built-in)

The `venv` module is Python's built-in virtual environment tool:

```bash
# Create a virtual environment
python3 -m venv myproject_env

# Activate the environment
# On macOS/Linux:
source myproject_env/bin/activate

# On Windows:
myproject_env\Scripts\activate

# On Windows (PowerShell):
myproject_env\Scripts\Activate.ps1

# Verify activation (prompt should change)
which python  # Should show path to venv
python --version

# Install packages (only affects this environment)
pip install requests pandas numpy

# List installed packages
pip list

# Create requirements file
pip freeze > requirements.txt

# Deactivate environment
deactivate
```

### 🚀 Advanced Virtual Environment Management

#### 🔧 Using virtualenv (Third-party)

```bash
# Install virtualenv
pip install virtualenv

# Create environment with specific Python version
virtualenv -p python3.10 myproject_env

# Create environment with system site packages
virtualenv --system-site-packages myproject_env

# Create environment without pip
virtualenv --no-pip myproject_env
```

#### 🐍 Using conda

Conda provides both package and environment management:

```bash
# Install Miniconda or Anaconda
# Then create environment
conda create -n myproject python=3.10

# Activate environment
conda activate myproject

# Install packages
conda install numpy pandas matplotlib
pip install requests  # Mix conda and pip if needed

# Export environment
conda env export > environment.yml

# Create from environment file
conda env create -f environment.yml

# List environments
conda env list

# Remove environment
conda env remove -n myproject
```

#### 📦 Using pipenv

Combines pip and virtualenv functionality:

```bash
# Install pipenv
pip install pipenv

# Create Pipfile and virtual environment
pipenv install

# Install packages
pipenv install requests
pipenv install pytest --dev  # Development dependency

# Activate shell
pipenv shell

# Run commands in environment
pipenv run python script.py

# Install from Pipfile
pipenv install --dev  # Include dev dependencies

# Generate requirements.txt
pipenv requirements > requirements.txt
```

#### 🎭 Using poetry (Modern Alternative)

Poetry provides advanced dependency management:

```bash
# Install poetry
curl -sSL https://install.python-poetry.org | python3 -

# Create new project
poetry new myproject
cd myproject

# Add dependencies
poetry add requests
poetry add pytest --group dev

# Install dependencies
poetry install

# Activate environment
poetry shell

# Run commands
poetry run python script.py

# Export requirements
poetry export -f requirements.txt --output requirements.txt
```

### ⭐ Virtual Environment Best Practices

#### 1. 📂 Project Structure

```
myproject/
├── venv/                    # Virtual environment (git-ignored)
├── src/                     # Source code
│   └── myproject/
├── tests/                   # Test files
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── .env                     # Environment variables
├── .gitignore              # Git ignore file
└── README.md               # Project documentation
```

#### 2. 📋 Requirements Management

```bash
# Create separate requirements files
# requirements.txt (production)
requests==2.28.1
pandas==1.5.2
numpy==1.24.0

# requirements-dev.txt (development)
-r requirements.txt
pytest==7.2.0
black==22.12.0
mypy==0.991
flake8==6.0.0
```

#### 3. Environment Variables

```bash
# .env file (never commit to git)
DATABASE_URL=postgresql://localhost:5432/mydb
API_KEY=your_secret_key_here
DEBUG=True

# Load in Python using python-dotenv
pip install python-dotenv
```

```python
# In your Python code
import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv('DATABASE_URL')
api_key = os.getenv('API_KEY')
debug = os.getenv('DEBUG', 'False').lower() == 'true'
```

#### 4. Activation Scripts

Create convenience scripts for environment management:

```bash
# activate.sh (macOS/Linux)
#!/bin/bash
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
echo "Virtual environment activated for $(pwd)"

# activate.bat (Windows)
@echo off
call venv\Scripts\activate.bat
set PYTHONPATH=%PYTHONPATH%;%CD%\src
echo Virtual environment activated for %CD%
```

### Virtual Environment Automation

#### Using direnv

Automatically activate/deactivate environments when entering directories:

```bash
# Install direnv
brew install direnv  # macOS
sudo apt install direnv  # Ubuntu

# Add to shell (add to ~/.bashrc or ~/.zshrc)
eval "$(direnv hook bash)"  # or zsh

# Create .envrc in project directory
echo "source venv/bin/activate" > .envrc
direnv allow
```

#### Using autoenv

```bash
# Install autoenv
pip install autoenv

# Add to shell
echo "source ~/.local/bin/activate.sh" >> ~/.bashrc

# Create .env file in project
echo "source venv/bin/activate" > .env
```

### Docker Integration

Combine virtual environments with Docker for ultimate isolation:

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ .

CMD ["python", "main.py"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    volumes:
      - .:/app
    environment:
      - PYTHONPATH=/app/src
    ports:
      - "8000:8000"
```

### Troubleshooting Virtual Environments

#### Common Issues and Solutions

1. **Permission Denied on Windows**
   ```powershell
   # Enable script execution
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **Wrong Python Version**
   ```bash
   # Specify Python version explicitly
   python3.10 -m venv venv
   # or
   virtualenv -p python3.10 venv
   ```

3. **SSL Certificate Issues**
   ```bash
   # Upgrade pip and certificates
   pip install --upgrade pip
   pip install --upgrade certifi
   ```

4. **Path Issues**
   ```bash
   # Check Python path
   python -c "import sys; print(sys.path)"
   
   # Add to PYTHONPATH
   export PYTHONPATH="${PYTHONPATH}:/path/to/your/project"
   ```

5. **Corrupted Environment**
   ```bash
   # Remove and recreate
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### IDE Integration

#### VS Code
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.envFile": "${workspaceFolder}/.env"
}
```

#### PyCharm
1. File → Settings → Project → Python Interpreter
2. Add Interpreter → Existing environment
3. Select `venv/bin/python` (or `venv\Scripts\python.exe` on Windows)

#### Vim/Neovim
```vim
" .vimrc or init.vim
let g:python3_host_prog = './venv/bin/python'
```

### Virtual Environment Templates

#### Basic Project Template

```bash
#!/bin/bash
# create_python_project.sh

PROJECT_NAME=$1
if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: $0 <project_name>"
    exit 1
fi

# Create project structure
mkdir $PROJECT_NAME
cd $PROJECT_NAME

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Create basic structure
mkdir -p src/$PROJECT_NAME tests docs
touch src/$PROJECT_NAME/__init__.py
touch tests/__init__.py

# Create requirements files
cat > requirements.txt << EOF
# Production dependencies
requests>=2.28.0
EOF

cat > requirements-dev.txt << EOF
-r requirements.txt
# Development dependencies
pytest>=7.0.0
black>=22.0.0
mypy>=0.990
flake8>=5.0.0
pytest-cov>=4.0.0
EOF

# Create configuration files
cat > .gitignore << EOF
# Virtual environment
venv/
env/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.coverage
.pytest_cache/
htmlcov/

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF

cat > .env.example << EOF
# Copy to .env and fill in your values
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
SECRET_KEY=your-secret-key-here
EOF

cat > pyproject.toml << EOF
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "$PROJECT_NAME"
version = "0.1.0"
description = "A Python project"
authors = [{name = "Your Name", email = "your.email@example.com"}]
readme = "README.md"
requires-python = ">=3.8"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=22.0.0",
    "mypy>=0.990",
    "flake8>=5.0.0",
    "pytest-cov>=4.0.0",
]

[tool.black]
line-length = 88
target-version = ['py38']

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --cov=src"
EOF

# Install development dependencies
pip install -r requirements-dev.txt

echo "Project $PROJECT_NAME created successfully!"
echo "Activate with: source venv/bin/activate"
```

### Monitoring and Maintenance

#### Environment Health Checks

```python
# check_env.py
import sys
import subprocess
import pkg_resources
from pathlib import Path

def check_virtual_env():
    """Check if we're in a virtual environment."""
    return hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )

def check_outdated_packages():
    """Check for outdated packages."""
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'list', '--outdated'],
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception as e:
        return f"Error checking packages: {e}"

def check_requirements_sync():
    """Check if installed packages match requirements."""
    req_file = Path('requirements.txt')
    if not req_file.exists():
        return "No requirements.txt found"
    
    # Parse requirements
    with open(req_file) as f:
        requirements = f.read().splitlines()
    
    # Check installed packages
    installed = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    
    issues = []
    for req in requirements:
        if '==' in req:
            name, version = req.split('==')
            if name.lower() in installed:
                if installed[name.lower()] != version:
                    issues.append(f"{name}: required {version}, installed {installed[name.lower()]}")
            else:
                issues.append(f"{name}: required but not installed")
    
    return issues if issues else "All requirements satisfied"

if __name__ == "__main__":
    print(f"Virtual environment: {check_virtual_env()}")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print("\nOutdated packages:")
    print(check_outdated_packages())
    print("\nRequirements check:")
    print(check_requirements_sync())
```

#### Automated Updates

```bash
#!/bin/bash
# update_env.sh

echo "Updating virtual environment..."

# Activate virtual environment
source venv/bin/activate

# Update pip itself
pip install --upgrade pip

# Update all packages
pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U

# Update requirements file
pip freeze > requirements.txt

echo "Environment updated successfully!"
```

## Comparison Summary

### Python vs Java Environment Management

| Aspect | Python | Java |
|--------|--------|------|
| **Environment Isolation** | Virtual environments (venv, conda) | JVM classpath, Docker |
| **Dependency Management** | pip, poetry, pipenv | Maven, Gradle, SBT |
| **Version Management** | pyenv, conda | SDKMAN, jenv |
| **Build Tools** | setup.py, pyproject.toml | pom.xml, build.gradle |
| **Package Registry** | PyPI | Maven Central |

### Python vs Go Environment Management

| Aspect | Python | Go |
|--------|--------|-----|
| **Module System** | Virtual environments | Go modules (go.mod) |
| **Dependency Resolution** | pip resolver | Go module proxy |
| **Versioning** | Semantic versioning | Semantic import versioning |
| **Workspace** | Virtual environment | Go workspace (go.work) |
| **Build Caching** | pip cache | Go build cache |

## Next Steps

With your virtual environment set up, you're ready to:

1. **Explore Python syntax** - Move to the [Basic Syntax](../02_basic_syntax/) section
2. **Install development tools** - Set up linting, formatting, and testing tools
3. **Configure your IDE** - Integrate virtual environment with your preferred editor
4. **Start coding** - Begin with simple Python programs

Remember: Always work within virtual environments for Python development. This practice will save you countless hours of debugging dependency issues later! 