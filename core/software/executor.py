"""
Tool Executor — Safe Shell Command Runner & Build Pipeline.
Allows the agent to compile code (gcc, cmake, platformio), run scripts,
and analyze build output within a sandboxed subprocess.
"""

import os
import subprocess
import time
import shlex
from typing import Dict, Any, Optional, List

# Commands that are NEVER allowed (destructive operations)
BLOCKED_COMMANDS = ["rm -rf /", "mkfs", "dd if=", ":(){ :|:& };:", "shutdown", "reboot"]

# Whitelisted safe command prefixes for embedded development
SAFE_PREFIXES = [
    "gcc", "g++", "make", "cmake", "ninja",
    "platformio", "pio", "idf.py",
    "python", "python3", "pip",
    "cat", "head", "tail", "wc", "grep", "find", "ls", "tree",
    "git status", "git log", "git diff", "git branch",
    "arm-none-eabi-gcc", "avr-gcc",
    "openocd", "esptool",
]

def is_command_safe(command: str) -> bool:
    """Checks if a command is safe to execute."""
    cmd_lower = command.strip().lower()
    for blocked in BLOCKED_COMMANDS:
        if blocked in cmd_lower:
            return False
    return True

def execute_command(
    command: str,
    cwd: Optional[str] = None,
    timeout_seconds: int = 60,
    env_vars: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Executes a shell command in a subprocess and returns structured output.
    Captures stdout, stderr, return code, and execution time.
    """
    if not is_command_safe(command):
        return {
            "status": "blocked",
            "error": f"Command blocked for safety: '{command}'",
            "return_code": -1
        }

    working_dir = cwd or os.getcwd()
    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)

    start_time = time.time()

    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=working_dir,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            env=env
        )

        elapsed_ms = round((time.time() - start_time) * 1000, 1)

        return {
            "status": "success" if result.returncode == 0 else "error",
            "command": command,
            "cwd": working_dir,
            "return_code": result.returncode,
            "stdout": result.stdout[-3000:] if result.stdout else "",
            "stderr": result.stderr[-2000:] if result.stderr else "",
            "execution_time_ms": elapsed_ms
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "command": command,
            "error": f"Command timed out after {timeout_seconds}s",
            "return_code": -1
        }
    except Exception as e:
        return {
            "status": "error",
            "command": command,
            "error": str(e),
            "return_code": -1
        }

def compile_c(source_file: str, output_file: Optional[str] = None, flags: str = "-Wall -Wextra") -> Dict[str, Any]:
    """Compiles a C source file with gcc."""
    if output_file is None:
        output_file = os.path.splitext(source_file)[0]
    cmd = f"gcc {flags} -o {shlex.quote(output_file)} {shlex.quote(source_file)}"
    return execute_command(cmd, cwd=os.path.dirname(source_file) or ".")

def compile_cpp(source_file: str, output_file: Optional[str] = None, flags: str = "-Wall -Wextra -std=c++17") -> Dict[str, Any]:
    """Compiles a C++ source file with g++."""
    if output_file is None:
        output_file = os.path.splitext(source_file)[0]
    cmd = f"g++ {flags} -o {shlex.quote(output_file)} {shlex.quote(source_file)}"
    return execute_command(cmd, cwd=os.path.dirname(source_file) or ".")

def run_make(target: str = "", cwd: str = ".") -> Dict[str, Any]:
    """Runs make with optional target in the specified directory."""
    cmd = f"make {target}".strip()
    return execute_command(cmd, cwd=cwd)

def run_platformio(command: str = "run", cwd: str = ".") -> Dict[str, Any]:
    """Runs PlatformIO CLI command (build, upload, test, monitor)."""
    cmd = f"platformio {command}"
    return execute_command(cmd, cwd=cwd, timeout_seconds=120)
