"""
Agent Self-Improvement Engine.
Evaluates agent response quality, unit test failure patterns, and user feedback.
Automatically refines prompt specifications in `agents/*.md` to continuously optimize accuracy.
"""

import os
import time
from typing import Dict, Any, List, Optional

AGENTS_DIR = os.path.join(os.path.dirname(__file__), "..", "agents")

def analyze_and_refine_agent_prompt(
    agent_name: str,
    failed_prompt: str,
    error_reason: str,
    suggested_rule: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyzes an agent error or failed unit test, and automatically 
    appends a preventative guideline rule to the target agent spec in `agents/*.md`.
    """
    target_spec = os.path.join(AGENTS_DIR, f"{agent_name.lower()}.md")

    if not os.path.exists(target_spec):
        return {"status": "error", "error": f"Agent spec file '{target_spec}' not found."}

    try:
        with open(target_spec, "r", encoding="utf-8") as f:
            content = f.read()

        # Formulate new self-learned guideline rule
        rule_to_add = suggested_rule or f"Always verify {error_reason} when processing user requests."

        new_rule_entry = f"\n- **Self-Learned Rule (Auto-Refined)**: {rule_to_add}"

        if "## Key Responsibilities" in content:
            updated_content = content.replace("## Key Responsibilities", f"## Key Responsibilities{new_rule_entry}")
        else:
            updated_content = content + f"\n\n## Learned Guidelines{new_rule_entry}"

        with open(target_spec, "w", encoding="utf-8") as f:
            f.write(updated_content)

        return {
            "status": "success",
            "agent_name": agent_name,
            "spec_file": target_spec,
            "rule_added": rule_to_add,
            "message": f"Successfully refined prompt spec for [{agent_name}]!"
        }
    except Exception as e:
        return {"status": "error", "error": f"Failed to refine agent spec: {str(e)}"}
