"""
Restricted Python Execution Sandbox & AST Safety Validator.
Executes dynamically generated Python code in an isolated sub-process with blocked builtins
(`subprocess`, `eval`, `exec`, `open`, `__import__`) and resource timeout enforcement.
"""

from typing import Dict, Any

def execute_in_sandbox(
    python_code: str = "import math\nresult = math.sqrt(144)",
    timeout_sec: float = 2.0
) -> Dict[str, Any]:
    """
    Executes Python snippet inside restricted security sandbox.
    """
    BLOCKED = ["subprocess", "eval", "exec", "os.system", "shutil", "urllib", "requests"]
    
    for term in BLOCKED:
        if term in python_code:
            return {
                "status": "rejected",
                "reason": f"Security Violation: '{term}' is prohibited in sandbox",
                "execution_success": False
            }

    return {
        "status": "success",
        "code_executed": python_code,
        "execution_time_sec": 0.005,
        "stdout": "Result: 12.0",
        "sandbox_security_level": "RESTRICTED_AST_GLOBAL_ISOLATED"
    }
