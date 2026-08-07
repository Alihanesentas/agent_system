import os
import sys
import time
import socket
import subprocess
import urllib.request

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def is_port_open(host: str = "127.0.0.1", port: int = 8000) -> bool:
    """Checks if a port is open and listening."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1.0)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

def ensure_services_running(verbose: bool = False):
    """
    Autonomous Service Manager. Automatically checks if FastAPI backend (Port 8000) 
    and React Dashboard (Port 5173) are running. If not, spawns them silently in the background!
    """
    python_bin = sys.executable or "python3"

    # 1. Check FastAPI Backend (Port 8000)
    if not is_port_open("127.0.0.1", 8000):
        if verbose:
            print("🚀 [Autonomous Manager]: Starting FastAPI Tracer Backend on Port 8000...")
        env = os.environ.copy()
        env["PYTHONPATH"] = PROJECT_ROOT
        subprocess.Popen(
            [python_bin, "-m", "uvicorn", "subagent_tracker.backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
            cwd=PROJECT_ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env,
            start_new_session=True
        )
        time.sleep(1.2)

    # 2. Check React Vite Dashboard (Port 5173)
    if not is_port_open("127.0.0.1", 5173):
        if verbose:
            print("🎨 [Autonomous Manager]: Starting React Web Dashboard on Port 5173...")
        frontend_dir = os.path.join(PROJECT_ROOT, "subagent_tracker", "frontend")
        if os.path.exists(frontend_dir):
            subprocess.Popen(
                ["npm", "run", "dev", "--", "--host", "127.0.0.1"],
                cwd=frontend_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
