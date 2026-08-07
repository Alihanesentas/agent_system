"""
Self-Healing Build Loop — Automated Code Compilation & Error Recovery.
Compiles C/C++/Python code. If a compilation or lint error occurs, 
captures the exact stderr error log, feeds it to the Software & Reviewer agents, 
auto-corrects the source code, and re-compiles until return_code == 0.
"""

import os
import time
from typing import Dict, Any, List, Optional
from core.executor import compile_c, compile_cpp, execute_command
from core.runner import run_agent_task

def auto_compile_and_fix(
    source_file: str,
    language: str = "c",
    max_retries: int = 3,
    model_name: str = "gpt-4o"
) -> Dict[str, Any]:
    """
    Autonomous Self-Healing Loop.
    Attempts build -> on error -> sends traceback to agent -> fixes code -> retries.
    """
    if not os.path.exists(source_file):
        return {"status": "error", "error": f"Source file '{source_file}' not found."}

    history: List[Dict[str, Any]] = []

    for attempt in range(1, max_retries + 1):
        # 1. Attempt Compilation
        if language.lower() == "c":
            res = compile_c(source_file)
        elif language.lower() in ["cpp", "c++"]:
            res = compile_cpp(source_file)
        else:
            # Python syntax check
            res = execute_command(f"python3 -m py_compile {source_file}")

        if res.get("status") == "success":
            return {
                "status": "success",
                "attempts": attempt,
                "source_file": source_file,
                "history": history,
                "message": f"Build succeeded on attempt {attempt}!"
            }

        # 2. Build Failed — Capture error log
        stderr_log = res.get("stderr") or res.get("stdout") or res.get("error", "Unknown error")
        history.append({"attempt": attempt, "stderr": stderr_log})

        print(f"⚠️ [Self-Healing Attempt {attempt}/{max_retries} Failed]: Compiler error detected. Invoking Reviewer Agent...")

        # Read current source code
        with open(source_file, "r", encoding="utf-8") as f:
            code_content = f.read()

        # 3. Formulate Prompt for Agent Repair
        fix_prompt = (
            f"The compilation of file '{source_file}' failed on attempt {attempt}.\n"
            f"COMPILER ERROR TRACEBACK:\n```\n{stderr_log}\n```\n\n"
            f"ORIGINAL CODE:\n```c\n{code_content}\n```\n\n"
            f"Please fix the code syntax and return ONLY the complete corrected source code wrapped in ```c ``` codeblock."
        )

        fixed_response = run_agent_task(
            agent_name="reviewer",
            user_prompt=fix_prompt,
            model_name=model_name,
            use_rag=False
        )

        # Extract fixed code from response
        corrected_code = _extract_code_block(fixed_response)
        if corrected_code:
            with open(source_file, "w", encoding="utf-8") as f:
                f.write(corrected_code)
            print(f"🔧 [Self-Healing]: Applied corrected code patch to '{source_file}'. Retrying build...")
        else:
            print("⚠️ [Self-Healing]: Agent response did not contain a valid codeblock. Stopping.")
            break

    return {
        "status": "failed",
        "attempts": max_retries,
        "source_file": source_file,
        "history": history,
        "error": "Failed to resolve compilation errors after maximum retries."
    }

def _extract_code_block(response: str) -> Optional[str]:
    """Extracts code block content from markdown text."""
    if "```" not in response:
        return None

    lines = response.split("\n")
    in_block = False
    block_lines = []

    for line in lines:
        if line.strip().startswith("```"):
            if in_block:
                in_block = False
                break
            else:
                in_block = True
                continue
        if in_block:
            block_lines.append(line)

    return "\n".join(block_lines) if block_lines else None
