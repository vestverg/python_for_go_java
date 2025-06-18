# Getting Started Examples

This directory contains practical examples and tools for Python development setup, with a focus on virtual environment management.

## Files Overview

### 1. `hello.py`
A simple "Hello, World!" program demonstrating:
- Basic Python syntax
- Print statements
- Comments and docstrings
- Script execution patterns

**Usage:**
```bash
python hello.py
```

### 2. `virtual_env_demo.py`
A comprehensive demonstration of virtual environment management concepts:
- Environment detection and analysis
- Package management utilities
- Project structure creation
- Tool comparisons (venv, conda, pipenv, poetry)
- Best practices for virtual environment usage

**Features:**
- Detects current virtual environment status
- Lists installed packages
- Shows site-packages directories
- Compares different virtual environment tools
- Demonstrates project creation patterns

**Usage:**
```bash
python virtual_env_demo.py
```

### 3. `create_project.sh` (Unix/Linux/macOS)
A comprehensive shell script that creates a complete Python project structure with:
- Virtual environment setup
- Modern project layout (src/ layout)
- Configuration files (pyproject.toml, .gitignore, etc.)
- Development dependencies
- Testing setup
- Git repository initialization
- Cross-platform activation scripts

**Features:**
- Python version detection and validation
- Comprehensive project structure
- Modern packaging configuration
- Development tool setup (black, mypy, pytest, etc.)
- Colored output and error handling
- Complete documentation generation

**Usage:**
```bash
# Create project with default Python version
./create_project.sh my_project

# Create project with specific Python version
./create_project.sh my_project 3.10
```

**Generated Project Structure:**
```
my_project/
├── src/my_project/          # Main package
│   ├── __init__.py
│   └── main.py
├── tests/                   # Test files
│   ├── __init__.py
│   └── test_main.py
├── docs/                    # Documentation
├── scripts/                 # Utility scripts
│   ├── activate.sh          # Enhanced activation script
│   └── activate.bat         # Windows activation script
├── venv/                    # Virtual environment
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── pyproject.toml          # Modern Python configuration
├── .gitignore              # Git ignore rules
├── .env.example            # Environment variables template
└── README.md               # Project documentation
```

### 4. `create_project.ps1` (Windows PowerShell)
Windows PowerShell version of the project creation script with:
- Windows-specific path handling
- PowerShell execution policy management
- Windows-style environment variable handling
- Python launcher (py) support
- Comprehensive error handling

**Features:**
- Automatic Python detection (python, py launcher)
- Windows-specific optimizations
- PowerShell-native error handling
- Complete project scaffolding
- Development environment setup

**Usage:**
```powershell
# Create project with default Python version
.\create_project.ps1 my_project

# Create project with specific Python version
.\create_project.ps1 my_project 3.10
```

## Virtual Environment Concepts Demonstrated

### 1. Environment Detection
```python
# Check if running in virtual environment
import sys
is_virtual = (
    hasattr(sys, 'real_prefix') or 
    (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
)
```

### 2. Package Management
```bash
# Create virtual environment
python -m venv myproject_env

# Activate environment
source myproject_env/bin/activate  # Unix/Linux/macOS
myproject_env\Scripts\activate     # Windows

# Install packages
pip install package_name

# Freeze dependencies
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt
```

### 3. Modern Project Structure
The examples demonstrate the modern Python project layout:
- `src/` layout for better testing and packaging
- Separate development and production dependencies
- Modern configuration with `pyproject.toml`
- Proper `.gitignore` for Python projects
- Environment variable management

### 4. Tool Comparisons

| Tool | Strengths | Use Cases |
|------|-----------|-----------|
| **venv** | Built-in, lightweight, simple | Learning, simple projects |
| **virtualenv** | More features, Python 2.7+ support | Legacy projects, advanced features |
| **conda** | Non-Python dependencies, scientific packages | Data science, research |
| **pipenv** | Pipfile format, automatic activation | Modern development workflows |
| **poetry** | Advanced dependency resolution, packaging | Library development, complex projects |

### 5. Best Practices Demonstrated

1. **Always use virtual environments** - Isolate project dependencies
2. **Separate requirements files** - Production vs development dependencies
3. **Version pinning** - Ensure reproducible builds
4. **Environment variables** - Use `.env` files for configuration
5. **Modern tooling** - Type checking, code formatting, testing
6. **Documentation** - Comprehensive README and docstrings
7. **Git integration** - Proper `.gitignore` and repository setup

## Integration with IDEs

### VS Code Configuration
The generated projects include VS Code settings:
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.envFile": "${workspaceFolder}/.env"
}
```

### PyCharm Setup
1. File → Settings → Project → Python Interpreter
2. Add Interpreter → Existing environment
3. Select `venv/bin/python` or `venv\Scripts\python.exe`

## Advanced Features

### Environment Health Monitoring
The `virtual_env_demo.py` script includes utilities for:
- Checking installed packages
- Detecting package conflicts
- Monitoring environment health
- Generating dependency reports

### Automation Scripts
Both creation scripts include:
- Automatic dependency installation
- Git repository initialization
- Pre-commit hook setup
- Development tool configuration
- Cross-platform compatibility

### Project Templates
The scripts create projects with:
- Modern packaging configuration
- Testing infrastructure
- Linting and formatting tools
- Type checking setup
- Documentation templates

## Troubleshooting

### Common Issues

1. **Permission denied on Windows**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **Wrong Python version**
   ```bash
   python3.10 -m venv venv  # Specify version explicitly
   ```

3. **Path issues**
   ```bash
   export PYTHONPATH="${PYTHONPATH}:/path/to/project/src"
   ```

4. **SSL certificate issues**
   ```bash
   pip install --upgrade pip certifi
   ```

### Environment Recovery
If a virtual environment becomes corrupted:
```bash
# Remove and recreate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Learning Path

1. **Start with `hello.py`** - Basic Python execution
2. **Run `virtual_env_demo.py`** - Understand virtual environments
3. **Create a test project** - Use creation scripts
4. **Explore project structure** - Understand modern layout
5. **Practice dependency management** - Add/remove packages
6. **Configure your IDE** - Set up development environment

## Resources

- [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)
- [pip Documentation](https://pip.pypa.io/en/stable/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Pipenv Documentation](https://pipenv.pypa.io/en/latest/)
- [Modern Python Packaging](https://packaging.python.org/) 