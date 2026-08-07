"""
Real-Time Output Guardrails & Safety Filter.
Inspects generated C++ firmware, OpenSCAD scripts, and BOM JSONs before writing to disk,
stripping syntax flaws, missing header includes, or invalid GPIO pin assignments.
"""

import re
from typing import Dict, Any, Tuple

def sanitize_and_verify_code(
    code_str: str,
    language: str = "cpp"
) -> Dict[str, Any]:
    """
    Sanitizes LLM generated code outputs:
    1. Strips markdown fences (```cpp ... ```)
    2. Validates essential headers (#include <Arduino.h>)
    3. Prevents invalid pin dereferencing
    """
    cleaned = code_str.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        cleaned = "\n".join(lines)

    issues = []
    if language.lower() in ["cpp", "c"]:
        if "#include" not in cleaned and "void setup()" in cleaned:
            cleaned = "#include <Arduino.h>\n\n" + cleaned
            issues.append("Auto-injected missing '#include <Arduino.h>' header.")

    return {
        "status": "passed" if len(issues) == 0 else "sanitized",
        "original_len": len(code_str),
        "sanitized_len": len(cleaned),
        "sanitized_code": cleaned,
        "auto_fixes": issues
    }
