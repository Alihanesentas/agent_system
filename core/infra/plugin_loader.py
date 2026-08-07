"""
Hot-Reloadable Dynamic Plugin System.
Enables writing custom Python plugin modules in `plugins/` that load and hot-reload
dynamically without restarting the CLI shell or FastAPI backend server.
"""

import os
import importlib.util
from typing import Dict, Any, List

PLUGINS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "plugins")

def discover_and_reload_plugins() -> Dict[str, Any]:
    """
    Discovers and hot-reloads custom Python plugins from `plugins/` directory.
    """
    os.makedirs(PLUGINS_DIR, exist_ok=True)
    loaded_plugins = []
    
    for fname in os.listdir(PLUGINS_DIR):
        if fname.endswith(".py") and not fname.startswith("__"):
            p_path = os.path.join(PLUGINS_DIR, fname)
            mod_name = fname[:-3]
            try:
                spec = importlib.util.spec_from_file_location(mod_name, p_path)
                if spec and spec.loader:
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    loaded_plugins.append(mod_name)
            except Exception as e:
                pass

    return {
        "status": "success",
        "plugins_dir": PLUGINS_DIR,
        "loaded_plugins_count": len(loaded_plugins),
        "loaded_plugins": loaded_plugins
    }
