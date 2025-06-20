# 📦 Modules & Packages - Knowledge Check

> **Organize your Python code!** 🎯  
> Master imports, packages, and Python's ecosystem management.

---

## 📊 **Progress Tracker**
**Section:** Modules & Packages | **Questions:** 6 | **Difficulty:** Intermediate | **Time:** ~5 min

---

### 🎯 **Question 1 of 6**
**How do you import a module in Python?**

```python
# Module import patterns:
# Java: import java.util.List;
# Go: import "fmt"
# Python: ???
```

**A.** `import math`  
**B.** `include math`  
**C.** `using math`  

---

### 🎯 **Question 2 of 6**
**What makes a directory a Python package?**

```python
# Package structure:
mypackage/
├── __init__.py    # This file!
├── module1.py
└── subpackage/
    ├── __init__.py
    └── module2.py
```

**A.** Having Python files in it  
**B.** The `__init__.py` file  
**C.** Being named with lowercase  

---

### 🎯 **Question 3 of 6**
**How do you import specific functions from a module?**

```python
# Instead of importing everything:
import math
result = math.sqrt(16)

# Import just what you need:
??? math import sqrt
result = sqrt(16)
```

**A.** `from math import sqrt`  
**B.** `import sqrt from math`  
**C.** `using math.sqrt`  

---

### 🎯 **Question 4 of 6**
**What controls Python's module search path?**

```python
import sys
print(sys.path)  # Shows search paths

# What environment variable affects this?
```

**A.** `PYTHONPATH`  
**B.** `PYTHON_VERSION`  
**C.** `VIRTUAL_ENV`  

---

### 🎯 **Question 5 of 6**
**Which file defines modern Python project metadata?**

```toml
# Modern Python packaging:
[build-system]
requires = ["setuptools", "wheel"]

[project]
name = "my-awesome-package"
version = "1.0.0"
```

**A.** `pyproject.toml`  
**B.** `requirements.txt`  
**C.** `setup.cfg`  

---

### 🎯 **Question 6 of 6**
**What's the difference between relative and absolute imports?**

```python
# In mypackage/submodule.py:

# Absolute import:
from mypackage.utils import helper

# Relative import:
from .utils import helper  # Same package
from ..parent import something  # Parent package
```

**A.** No difference  
**B.** Relative uses dots (.), absolute uses full path  
**C.** Relative is deprecated

---

## 🎉 **Package Architecture Expert!**

### 📦 **Python Package Ecosystem:**
- **PyPI** → 400,000+ packages available  
- **pip** → Package installer and dependency manager
- **Virtual environments** → Isolated project dependencies
- **Modern packaging** → `pyproject.toml` replaces `setup.py`

### 🔄 **vs Other Languages:**
| Feature | Java | Go | Python |
|---------|------|----|---------| 
| **Package manager** | Maven/Gradle | `go mod` | `pip` |
| **Registry** | Maven Central | Go modules | PyPI |
| **Virtual envs** | ❌ | ❌ | ✅ |
| **Relative imports** | ✅ | ✅ | ✅ |

### 📈 **Next Steps:**
- ✅ **Package pro?** → Explore [Concurrency](../07_concurrency/)
- 🔍 **See structure?** → Check [mypackage](./examples/mypackage/)
- 🚀 **Publish packages?** → Learn about PyPI and twine

### 🔍 **Answer Key:**
*Test your Python packaging knowledge!*

<details>
<summary>🔓 Show Answers</summary>

1. **A** - `import math` is the standard import syntax
2. **B** - `__init__.py` file marks a directory as a package
3. **A** - `from module import function` imports specific items
4. **A** - `PYTHONPATH` environment variable controls search paths
5. **A** - `pyproject.toml` is the modern packaging standard (PEP 518)
6. **B** - Relative imports use dots, absolute use full module paths

**💡 Pro tips:**
- Use virtual environments for every project
- Prefer absolute imports for clarity
- Follow PEP 8 for package naming (lowercase_with_underscores)

</details>

---

*📦 **Code organization:** Good structure today saves hours tomorrow!* ✨🐍 

## 🌟 Expert Challenge

**Question**: Create a plugin system that combines Python's import hooks with Go's plugin system and Java's ServiceLoader. Your solution should:

1. Implement a custom import hook that:
   - Loads plugins from a directory structure
   - Supports hot-reloading of plugins
   - Validates plugin interfaces
   - Handles versioning and dependencies

2. Create a package management system that:
   - Uses namespace packages
   - Supports lazy loading
   - Handles circular dependencies
   - Provides plugin discovery

**Hint**: Look into `importlib.abc`, `sys.meta_path`, `pkgutil.extend_path`, and `importlib.util.spec_from_file_location`.

<details>
<summary>Show Answer</summary>

```python
import importlib.abc
import importlib.util
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Type
import warnings

class PluginSpec:
    def __init__(self, name: str, version: str, dependencies: List[str]):
        self.name = name
        self.version = version
        self.dependencies = dependencies

class PluginFinder(importlib.abc.MetaPathFinder):
    def __init__(self, plugin_dir: Path):
        self.plugin_dir = plugin_dir
        self.loaded_plugins: Dict[str, Any] = {}
        self._watch_timestamps: Dict[str, float] = {}
    
    def find_spec(
        self,
        fullname: str,
        path: Optional[List[str]] = None,
        target: Optional[Any] = None
    ) -> Optional[importlib.machinery.ModuleSpec]:
        if not fullname.startswith("plugins."):
            return None
        
        plugin_name = fullname.split(".")[-1]
        plugin_path = self.plugin_dir / f"{plugin_name}.py"
        
        if not plugin_path.exists():
            return None
        
        # Check if plugin needs reloading
        timestamp = plugin_path.stat().st_mtime
        if (plugin_name in self._watch_timestamps and 
            timestamp > self._watch_timestamps[plugin_name]):
            if plugin_name in self.loaded_plugins:
                del self.loaded_plugins[plugin_name]
                del sys.modules[fullname]
        
        self._watch_timestamps[plugin_name] = timestamp
        
        spec = importlib.util.spec_from_file_location(
            fullname,
            plugin_path,
            loader=PluginLoader(plugin_path, fullname),
            submodule_search_locations=None
        )
        
        return spec

class PluginLoader(importlib.abc.Loader):
    def __init__(self, path: Path, fullname: str):
        self.path = path
        self.fullname = fullname
    
    def create_module(self, spec: importlib.machinery.ModuleSpec) -> Optional[Any]:
        return None  # Use default module creation
    
    def exec_module(self, module: Any) -> None:
        # Load and validate plugin spec
        code = self.path.read_text()
        if "PLUGIN_SPEC" not in code:
            raise ImportError(
                f"Plugin {self.fullname} missing PLUGIN_SPEC declaration"
            )
        
        # Execute the module
        exec(code, module.__dict__)
        
        # Validate plugin spec
        spec = module.PLUGIN_SPEC
        if not isinstance(spec, PluginSpec):
            raise ImportError(
                f"Plugin {self.fullname} has invalid PLUGIN_SPEC"
            )
        
        # Check dependencies
        for dep in spec.dependencies:
            try:
                importlib.import_module(dep)
            except ImportError:
                raise ImportError(
                    f"Plugin {self.fullname} missing dependency: {dep}"
                )

class PluginManager:
    def __init__(self, plugin_dir: str):
        self.plugin_dir = Path(plugin_dir)
        self.plugin_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up import hook
        self.finder = PluginFinder(self.plugin_dir)
        sys.meta_path.insert(0, self.finder)
        
        # Set up namespace package
        plugins_init = self.plugin_dir.parent / "plugins" / "__init__.py"
        plugins_init.parent.mkdir(parents=True, exist_ok=True)
        plugins_init.touch()
    
    def discover_plugins(self) -> Dict[str, PluginSpec]:
        plugins = {}
        for plugin_file in self.plugin_dir.glob("*.py"):
            plugin_name = plugin_file.stem
            try:
                module = importlib.import_module(f"plugins.{plugin_name}")
                plugins[plugin_name] = module.PLUGIN_SPEC
            except Exception as e:
                warnings.warn(f"Failed to load plugin {plugin_name}: {e}")
        return plugins
    
    def get_plugin(self, name: str) -> Any:
        """Get a plugin by name, loading it if necessary"""
        if name not in self.finder.loaded_plugins:
            module = importlib.import_module(f"plugins.{name}")
            self.finder.loaded_plugins[name] = module
        return self.finder.loaded_plugins[name]

# Example usage:
# Create plugin directory structure
plugin_dir = Path("plugins")
plugin_dir.mkdir(exist_ok=True)

# Create a sample plugin
sample_plugin = """
from typing import Dict, Any

class SamplePlugin:
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {k.upper(): v * 2 for k, v in data.items()}

PLUGIN_SPEC = PluginSpec(
    name="sample",
    version="1.0.0",
    dependencies=["typing"]
)

plugin = SamplePlugin()
"""

(plugin_dir / "sample.py").write_text(sample_plugin)

# Initialize plugin manager
manager = PluginManager("plugins")

# Discover and use plugins
plugins = manager.discover_plugins()
print(f"Discovered plugins: {plugins}")

# Use a plugin
plugin_module = manager.get_plugin("sample")
result = plugin_module.plugin.process({"test": 42})
print(f"Plugin result: {result}")  # {"TEST": 84}
```

Key differences from Go/Java:
1. Python's import hooks are more flexible than Go's plugin system
2. Dynamic loading and reloading is built into Python's import machinery
3. Namespace packages provide better organization than Java's ServiceLoader
4. Python's module system handles circular dependencies more gracefully
5. Hot-reloading is possible without special tooling
6. Plugin validation can be done at runtime with full access to the type system

</details> 