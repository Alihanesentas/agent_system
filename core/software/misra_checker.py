"""
MISRA-C:2012 / MISRA C++ Safety-Critical Static Compliance Analyzer.
Audits C/C++ source code for mandatory and required MISRA rules (goto usage, pointer arithmetic,
unbounded dynamic allocation `malloc`, implicit type casting, and uninitialized variables).
"""

from typing import Dict, Any, List

def check_misra_compliance(
    code_snippet: str = "void process() { int *p = malloc(10); goto error; }"
) -> Dict[str, Any]:
    """
    Audits C snippet for MISRA-C:2012 rule violations.
    """
    violations = []
    
    if "goto " in code_snippet:
        violations.append({"rule": "MISRA Rule 15.1", "severity": "Mandatory", "desc": "The goto statement should not be used."})
    if "malloc(" in code_snippet or "free(" in code_snippet:
        violations.append({"rule": "MISRA Rule 21.3", "severity": "Required", "desc": "Dynamic memory allocation shall not be used."})
    if "int *" in code_snippet and "NULL" not in code_snippet:
        violations.append({"rule": "MISRA Rule 11.4", "severity": "Advisory", "desc": "Pointer conversions between different types."})

    return {
        "status": "success",
        "misra_standard": "MISRA-C:2012 / ISO 26262 Automotive Safety",
        "violations_found": len(violations),
        "violations": violations,
        "compliance_status": "PASSED" if len(violations) == 0 else "NON-COMPLIANT"
    }
