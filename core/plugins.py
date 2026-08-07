"""
Plugin Architecture — Extensible Tool Registration System.
Allows adding new tools (SPICE, CAD, slicer, custom APIs) 
as drop-in plugins without modifying core code.
"""

import os
import importlib
import json
from typing import Dict, Any, List, Optional, Callable

# Global plugin registry
_plugins: Dict[str, Dict[str, Any]] = {}

PLUGINS_DIR = os.path.join(os.path.dirname(__file__), "..", "plugins")

def register_plugin(name: str, description: str, handler: Callable, category: str = "tool"):
    """
    Registers a plugin function that can be called by agents.
    
    Args:
        name: Unique plugin name (e.g., 'spice_simulate')
        description: Human-readable description of what the plugin does
        handler: Callable function that implements the plugin logic
        category: Plugin category ('tool', 'api', 'analyzer', 'formatter')
    """
    _plugins[name] = {
        "name": name,
        "description": description,
        "handler": handler,
        "category": category
    }

def execute_plugin(name: str, **kwargs) -> Dict[str, Any]:
    """Executes a registered plugin by name with keyword arguments."""
    if name not in _plugins:
        return {"error": f"Plugin '{name}' not found. Available: {list(_plugins.keys())}"}

    try:
        result = _plugins[name]["handler"](**kwargs)
        return {"status": "success", "plugin": name, "result": result}
    except Exception as e:
        return {"status": "error", "plugin": name, "error": str(e)}

def list_plugins() -> List[Dict[str, str]]:
    """Lists all registered plugins with their descriptions."""
    return [
        {"name": p["name"], "description": p["description"], "category": p["category"]}
        for p in _plugins.values()
    ]

def load_plugins_from_dir():
    """
    Auto-discovers and loads plugins from the plugins/ directory.
    Each plugin file must have a `register()` function that calls `register_plugin()`.
    """
    if not os.path.exists(PLUGINS_DIR):
        os.makedirs(PLUGINS_DIR, exist_ok=True)
        # Create a sample plugin template
        sample = os.path.join(PLUGINS_DIR, "example_plugin.py")
        if not os.path.exists(sample):
            with open(sample, "w") as f:
                f.write('''"""Example Plugin — Template for creating custom agent plugins."""

from core.plugins import register_plugin

def my_custom_tool(input_text: str) -> str:
    """Your custom tool logic here."""
    return f"Processed: {input_text}"

def register():
    """Called automatically when plugins are loaded."""
    register_plugin(
        name="example_tool",
        description="A sample plugin template for demonstration",
        handler=my_custom_tool,
        category="tool"
    )
''')
        return

    for fname in os.listdir(PLUGINS_DIR):
        if fname.endswith(".py") and not fname.startswith("_"):
            module_name = fname[:-3]
            try:
                spec = importlib.util.spec_from_file_location(
                    f"plugins.{module_name}",
                    os.path.join(PLUGINS_DIR, fname)
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, "register"):
                    module.register()
            except Exception as e:
                print(f"⚠️  Failed to load plugin '{fname}': {e}")
