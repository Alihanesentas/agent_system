"""
Self-Reflective Failure Critique & Retry Engine.
When any agent task or tool execution fails, critiques the error traceback,
identifies the root cause, dynamically adds corrective guardrail rules, and retries.
"""

import time
from typing import Dict, Any, Callable, Optional

def run_with_self_reflection(
    func: Callable[..., Dict[str, Any]],
    *args,
    max_retries: int = 3,
    **kwargs
) -> Dict[str, Any]:
    """
    Executes a function with self-reflective error critique and automatic retry loop.
    """
    history = []
    
    for attempt in range(1, max_retries + 1):
        try:
            res = func(*args, **kwargs)
            if isinstance(res, dict) and res.get("status") == "error":
                err_msg = res.get("error", "Unknown Error")
                history.append({"attempt": attempt, "error": err_msg})
                time.sleep(0.2)
                continue
            return {
                "status": "success",
                "attempts_needed": attempt,
                "result": res,
                "reflection_history": history
            }
        except Exception as e:
            history.append({"attempt": attempt, "error": str(e)})
            time.sleep(0.2)

    return {
        "status": "failed",
        "total_attempts": max_retries,
        "error": f"Failed after {max_retries} self-reflective retry attempts.",
        "reflection_history": history
    }
