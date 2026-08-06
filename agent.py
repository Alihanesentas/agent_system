#!/usr/bin/env python3
"""
Autonomous Coding Agent CLI (Claude CLI / Gemini CLI Style)
Reads/writes files in your project directory and automatically logs token usage & telemetry.
"""

import sys
import os
import argparse
import time
from typing import Dict, Any, List

# Import core tracer runner
from core.runner import run_agent_task, trace_agent

class AgentFileSystemTools:
    """Built-in file and shell execution tools for the CLI agent."""
    
    @staticmethod
    def read_file(file_path: str) -> str:
        """Reads contents of a file in the workspace."""
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' does not exist."
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    @staticmethod
    def write_file(file_path: str, content: str) -> str:
        """Writes or updates content to a file in the workspace."""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Successfully written {len(content)} bytes to '{file_path}'"
        except Exception as e:
            return f"Error writing file: {str(e)}"

    @staticmethod
    def list_dir(dir_path: str = ".") -> List[str]:
        """Lists directory contents."""
        try:
            return os.listdir(dir_path)
        except Exception as e:
            return [f"Error listing directory: {str(e)}"]

@trace_agent(agent_name="software", model_name="gpt-4o")
def execute_coding_task(prompt: str, target_file: str = None, new_content: str = None) -> str:
    """
    Simulates / executes an autonomous coding task with file manipulation 
    and automatically logs token telemetry.
    """
    tools = AgentFileSystemTools()
    log_output = []

    if target_file:
        if new_content:
            res = tools.write_file(target_file, new_content)
            log_output.append(f"[File Write]: {res}")
        else:
            content = tools.read_file(target_file)
            log_output.append(f"[File Read ({target_file})]: Read {len(content)} characters.")

    res_summary = f"Processed prompt: '{prompt}'. Actions: {'; '.join(log_output) if log_output else 'Analysis complete.'}"
    return res_summary

def main():
    parser = argparse.ArgumentParser(
        description="Autonomous Coding Agent CLI (Gemini CLI / Claude CLI style)"
    )
    parser.add_argument("prompt", nargs="?", help="Task prompt for the agent")
    parser.add_argument("--file", "-f", help="Target file path to read or write")
    parser.add_argument("--write", "-w", help="Content to write to target file")
    parser.add_argument("--model", "-m", default="gpt-4o", help="Model name (default: gpt-4o)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Launch interactive terminal REPL mode")

    args = parser.parse_args()

    print("\033[96m⚡ AUTONOMOUS AGENT CLI (Token Traced)\033[0m")
    print("-" * 50)

    if args.interactive:
        print("\033[93mEntering interactive agent mode... Type 'exit' to quit.\033[0m\n")
        while True:
            try:
                user_input = input("\033[92magent> \033[0m")
                if user_input.strip().lower() in ["exit", "quit"]:
                    break
                if not user_input.strip():
                    continue

                output = run_agent_task(
                    agent_name="software",
                    user_prompt=user_input,
                    model_name=args.model
                )
                print(f"\033[94m🤖 Response:\033[0m {output}\n")
            except KeyboardInterrupt:
                print("\nExiting interactive mode.")
                break
    elif args.prompt:
        output = execute_coding_task(
            prompt=args.prompt,
            target_file=args.file,
            new_content=args.write
        )
        print(f"\033[92m✅ Execution Complete:\033[0m {output}")
        print("\033[90m(Token usage & cost telemetry automatically logged to tracker database)\033[0m")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
