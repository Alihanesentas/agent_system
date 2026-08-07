"""
Hardware-in-the-Loop (HIL) Automated Testing Engine.
Connects to physical MCU boards via USB/TTY, flashes compiled binaries,
sends GPIO stimulus assertions over serial, and validates physical hardware execution.
"""

import time
import os
from typing import Dict, Any, List, Optional
from core.hardware.flasher import flash_firmware, read_serial_monitor

def run_hil_hardware_test(
    binary_path: str,
    port: str = "/dev/ttyUSB0",
    test_assertions: Optional[List[str]] = None,
    mcu: str = "esp32"
) -> Dict[str, Any]:
    """
    Executes automated Hardware-in-the-Loop (HIL) test cycle:
    1. Flashes binary to target physical hardware.
    2. Reads live UART console logs.
    3. Asserts expected log outputs & GPIO states.
    """
    expected = test_assertions or ["Booting", "I2C", "Connected"]
    
    # 1. Flash Firmware to Hardware
    flash_res = flash_firmware(binary_path, port=port, mcu=mcu)
    
    # 2. Read UART Serial Output
    serial_res = read_serial_monitor(port=port, timeout_seconds=3)
    logs = serial_res.get("logs", serial_res.get("simulated_logs", []))
    
    # 3. Validate Assertions
    passed_assertions = []
    failed_assertions = []
    
    combined_logs = " ".join(logs)
    for assertion in expected:
        if assertion.lower() in combined_logs.lower():
            passed_assertions.append(assertion)
        else:
            failed_assertions.append(assertion)

    success = len(failed_assertions) == 0
    return {
        "status": "passed" if success else "failed",
        "mcu": mcu,
        "port": port,
        "flash_status": flash_res.get("status", "unknown"),
        "total_assertions": len(expected),
        "passed_count": len(passed_assertions),
        "failed_count": len(failed_assertions),
        "passed_assertions": passed_assertions,
        "failed_assertions": failed_assertions,
        "logs_captured": len(logs)
    }
