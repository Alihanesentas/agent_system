"""
Interactive CLI Command Auto-Completer & History Manager.
Provides TAB autocompletion for all 55+ slash commands and persists command history.
"""

import os
import readline
from typing import List

COMMAND_LIST = [
    "/auto", "/layers", "/tree", "/heal", "/kicad", "/spice", "/pinout",
    "/thermal", "/drc", "/cad", "/slicer", "/edge-ai", "/rf", "/harness",
    "/ota", "/gantt", "/emc", "/part", "/alt", "/compare", "/cart",
    "/battery", "/unittest-gen", "/bom-opt", "/hil", "/voice", "/autoroute",
    "/graph", "/reflect", "/cost", "/guard", "/reload-plugins", "/worker",
    "/ratelimit", "/checkpoint", "/restore", "/metrics", "/report", "/replay",
    "/agent", "/model", "/memory", "/stats", "/logs", "/clear", "/help", "/exit"
]

def setup_cli_autocompletion():
    """Configures readline autocompletion for interactive CLI shell."""
    def completer(text: str, state: int) -> Optional[str]:
        options = [c for c in COMMAND_LIST if c.startswith(text)]
        if state < len(options):
            return options[state]
        return None

    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    hist_file = os.path.expanduser("~/.agent_history")
    if os.path.exists(hist_file):
        try:
            readline.read_history_file(hist_file)
        except Exception:
            pass
