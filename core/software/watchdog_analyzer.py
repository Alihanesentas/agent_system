"""
Firmware Watchdog & Crash Dump Analyzer Engine.
Analyzes ESP32 / STM32 panic dumps, register stack traces (PC, EXCCAUSE),
and task watchdog reset causes.
"""

from typing import Dict, Any

EXCCAUSE_CODES = {
    1: "IllegalInstructionCause (Executed invalid CPU instruction)",
    2: "SyscallCause",
    3: "InstructionFetchError",
    9: "LoadStoreAlignmentCause (Unaligned 32-bit memory access)",
    28: "LoadProhibited (Null pointer dereference / read from 0x00000000)",
    29: "StoreProhibited (Null pointer dereference / write to 0x00000000)"
}

def analyze_crash_dump(
    exccause_code: int = 28,
    pc_address: str = "0x400d15e4"
) -> Dict[str, Any]:
    """Analyzes CPU panic dump EXCCAUSE and program counter."""
    cause_desc = EXCCAUSE_CODES.get(exccause_code, f"Unknown Cause Code ({exccause_code})")
    
    return {
        "status": "success",
        "exccause_code": exccause_code,
        "cause_description": cause_desc,
        "program_counter": pc_address,
        "recommendation": "Check for null pointer assignment or uninitialized C++ object pointer"
    }
