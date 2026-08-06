from typing import Dict, Any, Tuple
import ast
from core.runner import run_agent_task

def analyze_code_quality(code_str: str) -> Tuple[bool, str]:
    """
    Performs static AST syntax verification on python code snippets.
    Returns (is_valid, error_or_success_msg).
    """
    if not code_str:
        return False, "Code string is empty."
    try:
        ast.parse(code_str)
        return True, "Syntax check passed cleanly."
    except SyntaxError as e:
        return False, f"SyntaxError on line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"AST Parse Error: {str(e)}"

def review_and_verify(
    task_prompt: str, 
    generated_code: str, 
    model_name: str = "gpt-4o"
) -> Dict[str, Any]:
    """
    Critic/Reviewer pattern: Inspects generated code for errors.
    If valid, passes through. If invalid, auto-refactors and logs reviewer activity.
    """
    is_valid, msg = analyze_code_quality(generated_code)

    if is_valid:
        return {
            "status": "passed",
            "verified_code": generated_code,
            "feedback": "Code passed static analysis cross-verification."
        }

    # Trigger Reviewer agent to fix detected syntax error
    reviewer_prompt = f"Fix the following python code for task '{task_prompt}'. Detected Error: {msg}\n\nCode:\n{generated_code}"
    
    refined_output = run_agent_task(
        agent_name="reviewer",
        user_prompt=reviewer_prompt,
        model_name=model_name
    )

    return {
        "status": "revised",
        "verified_code": refined_output,
        "feedback": f"Reviewer auto-corrected error: {msg}"
    }
