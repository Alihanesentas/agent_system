#!/usr/bin/env python3
"""
Interactive Autonomous Multi-Agent CLI Shell (Claude CLI / Gemini CLI Style)
Run directly via `agent` or `python agent.py`
"""

import sys
import os
import time
import argparse
from typing import Dict, Any, List, Optional

# Import core tracer runner
from core.runner import run_agent_task, trace_agent, log_agent_activity

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

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

def print_help():
    help_text = f"""
{Colors.BOLD}{Colors.CYAN}🤖 MULTI-AGENT INTERACTIVE SHELL COMMANDS:{Colors.RESET}
  {Colors.GREEN}/read <path>{Colors.RESET}         -> Reads a file in your project directory
  {Colors.GREEN}/write <path> <text>{Colors.RESET} -> Writes content to a file in your project directory
  {Colors.GREEN}/list [path]{Colors.RESET}        -> Lists files in project directory
  {Colors.GREEN}/agent <name>{Colors.RESET}       -> Switch active sub-agent (orchestrator, planner, software, tutor)
  {Colors.GREEN}/model <name>{Colors.RESET}       -> Switch model (gpt-4o, gpt-4o-mini, claude-3-5-sonnet, gemini-1.5-flash)
  {Colors.GREEN}/stats{Colors.RESET}              -> View live token, cost, and latency statistics
  {Colors.GREEN}/logs{Colors.RESET}               -> View recent activity trace logs
  {Colors.GREEN}/clear{Colors.RESET}              -> Clear terminal screen
  {Colors.GREEN}/help{Colors.RESET}               -> Show this help menu
  {Colors.GREEN}/exit{Colors.RESET}               -> Exit interactive shell
"""
    print(help_text)

def print_banner():
    banner = f"""
{Colors.CYAN}======================================================================{Colors.RESET}
{Colors.BOLD}{Colors.GREEN} 🤖 MULTI-AGENT AUTONOMOUS CLI SHELL (Gemini / Claude Style) {Colors.RESET}
{Colors.CYAN}======================================================================{Colors.RESET}
Type {Colors.YELLOW}/help{Colors.RESET} for slash commands. All actions are token-traced.
"""
    print(banner)

def start_interactive_shell(default_agent: str = "orchestrator", default_model: str = "gpt-4o"):
    print_banner()
    active_agent = default_agent
    active_model = default_model

    tools = AgentFileSystemTools()

    while True:
        try:
            prompt_str = f"{Colors.BOLD}{Colors.CYAN}[{active_agent.upper()} | {active_model}]{Colors.RESET} {Colors.GREEN}agent>{Colors.RESET} "
            user_input = input(prompt_str).strip()

            if not user_input:
                continue

            # Slash commands
            if user_input.startswith("/"):
                parts = user_input.split(maxsplit=2)
                cmd = parts[0].lower()

                if cmd in ["/exit", "/quit"]:
                    print(f"{Colors.YELLOW}Exiting agent shell. Goodbye!{Colors.RESET}")
                    break
                elif cmd == "/help":
                    print_help()
                elif cmd == "/clear":
                    os.system("cls" if os.name == "nt" else "clear")
                    print_banner()
                elif cmd == "/agent":
                    if len(parts) > 1:
                        active_agent = parts[1].lower()
                        print(f"{Colors.GREEN}Switched active agent to: {active_agent.upper()}{Colors.RESET}")
                    else:
                        print(f"Current agent: {active_agent}. Usage: /agent <orchestrator|planner|software|tutor>")
                elif cmd == "/model":
                    if len(parts) > 1:
                        active_model = parts[1].lower()
                        print(f"{Colors.GREEN}Switched active model to: {active_model}{Colors.RESET}")
                    else:
                        print(f"Current model: {active_model}. Usage: /model <model_name>")
                elif cmd == "/read":
                    if len(parts) > 1:
                        content = tools.read_file(parts[1])
                        print(f"{Colors.BLUE}--- FILE CONTENT ({parts[1]}) ---{Colors.RESET}\n{content}\n")
                    else:
                        print("Usage: /read <file_path>")
                elif cmd == "/write":
                    if len(parts) > 2:
                        res = tools.write_file(parts[1], parts[2])
                        print(f"{Colors.GREEN}✅ {res}{Colors.RESET}")
                    else:
                        print("Usage: /write <file_path> <content>")
                elif cmd == "/list":
                    target = parts[1] if len(parts) > 1 else "."
                    files = tools.list_dir(target)
                    print(f"{Colors.CYAN}Files in '{target}':{Colors.RESET} {', '.join(files)}")
                elif cmd == "/stats":
                    import cli
                    cli.cmd_stats(None)
                elif cmd == "/logs":
                    import cli
                    class DummyArgs:
                        limit = 5
                        agent = None
                    cli.cmd_logs(DummyArgs())
                else:
                    print(f"{Colors.RED}Unknown command '{cmd}'. Type /help for available commands.{Colors.RESET}")
            else:
                # Execute agent task
                print(f"{Colors.DIM}Thinking & executing task with [{active_agent}]...{Colors.RESET}")
                start_time = time.time()
                output = run_agent_task(
                    agent_name=active_agent,
                    user_prompt=user_input,
                    model_name=active_model
                )
                elapsed = round((time.time() - start_time) * 1000, 1)
                print(f"\n{Colors.BOLD}{Colors.PURPLE}🤖 [{active_agent.upper()} Response ({elapsed}ms)]:{Colors.RESET}")
                print(f"{output}\n")

        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Use /exit to quit.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Error executing command: {e}{Colors.RESET}")

def main():
    parser = argparse.ArgumentParser(description="Autonomous Multi-Agent CLI Shell")
    parser.add_argument("prompt", nargs="?", help="Optional initial task prompt")
    parser.add_argument("--agent", "-a", default="orchestrator", help="Active sub-agent name")
    parser.add_argument("--model", "-m", default="gpt-4o", help="Model name")

    args = parser.parse_args()

    if args.prompt:
        output = run_agent_task(agent_name=args.agent, user_prompt=args.prompt, model_name=args.model)
        print(output)
    else:
        start_interactive_shell(default_agent=args.agent, default_model=args.model)

if __name__ == "__main__":
    main()
