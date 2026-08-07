"""
CLI Shell Theme & Color Manager Engine.
Enables switching CLI color palettes (Cyberpunk, Matrix Green, Dracula Dark, Solarized)
dynamically via /theme <name> command.
"""

from typing import Dict, Any

CLI_THEMES = {
    "cyberpunk": {"primary": "\033[96m", "accent": "\033[95m", "success": "\033[92m", "warning": "\033[93m"},
    "matrix": {"primary": "\033[92m", "accent": "\033[32m", "success": "\033[92m", "warning": "\033[93m"},
    "dracula": {"primary": "\033[95m", "accent": "\033[94m", "success": "\033[92m", "warning": "\033[93m"},
    "solarized": {"primary": "\033[33m", "accent": "\033[36m", "success": "\033[32m", "warning": "\033[31m"}
}

active_theme_name = "cyberpunk"

def set_cli_theme(theme_name: str = "cyberpunk") -> Dict[str, Any]:
    """Sets active CLI color theme."""
    global active_theme_name
    t_lower = theme_name.lower()
    if t_lower in CLI_THEMES:
        active_theme_name = t_lower
        return {"status": "success", "active_theme": t_lower, "colors": CLI_THEMES[t_lower]}
    return {"status": "error", "message": f"Theme '{theme_name}' not found. Options: {list(CLI_THEMES.keys())}"}
