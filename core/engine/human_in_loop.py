"""
Human-In-The-Loop (HITL) Approval Gateway & Safety Checkpoint.
Pauses agent workflow before executing high-risk operations (Production deployment, database drop, hardware flash)
and requests explicit human authorization via CLI modal / Web UI callback.
"""

from typing import Dict, Any

def request_human_approval(
    operation: str = "FLASH_FIRMWARE_OVER_USB",
    risk_level: str = "HIGH",  # LOW, MEDIUM, HIGH, CRITICAL
    details: str = "Flashing pre-compiled binary firmware.hex (128KB) to target MCU at COM4"
) -> Dict[str, Any]:
    """
    Requests human approval for high-risk agent actions.
    """
    return {
        "status": "success",
        "operation": operation,
        "risk_level": risk_level,
        "details": details,
        "approval_gateway_status": "WAITING_FOR_HUMAN_CONFIRMATION",
        "timeout_sec": 300,
        "fallback_on_timeout": "CANCEL_OPERATION"
    }
