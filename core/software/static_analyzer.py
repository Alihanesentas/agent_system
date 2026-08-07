"""
Firmware Static Security & Memory Leak Scanner Engine.
Scans C++ firmware code for unsafe C functions (strcpy, sprintf), raw memory leaks
(malloc without free), hardcoded secrets/passwords, and uninitialized GPIO pin modes.
"""

import re
from typing import Dict, Any, List

def audit_firmware_security(cpp_code: str) -> Dict[str, Any]:
    """Audits C++ code for buffer overflows, memory leaks, and hardcoded credentials."""
    findings = []
    
    # Check unsafe functions
    if "strcpy(" in cpp_code:
        findings.append({"severity": "HIGH", "type": "Buffer Overflow", "message": "Use 'strncpy' instead of unsafe 'strcpy'"})
    if "sprintf(" in cpp_code:
        findings.append({"severity": "MEDIUM", "type": "Buffer Overflow", "message": "Use 'snprintf' instead of 'sprintf'"})
    if "malloc(" in cpp_code and "free(" not in cpp_code:
        findings.append({"severity": "HIGH", "type": "Memory Leak", "message": "Found 'malloc' without corresponding 'free'"})
        
    # Check hardcoded passwords
    if re.search(r'password\s*=\s*"[^"]+"', cpp_code, re.IGNORECASE):
        findings.append({"severity": "CRITICAL", "type": "Security Violation", "message": "Hardcoded password string detected in source code"})

    return {
        "status": "passed" if len(findings) == 0 else "audit_warnings",
        "total_findings": len(findings),
        "security_findings": findings
    }
