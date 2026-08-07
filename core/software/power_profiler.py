"""
Firmware Energy Consumption & Power Profile Analyzer Engine.
Calculates estimated current draw (mA), battery drainage curve, and deep sleep vs active state
power consumption for ESP32/STM32 firmware C++ code routines.
"""

import re
from typing import Dict, Any

def profile_firmware_power(
    cpp_code: str,
    battery_mah: float = 1200.0,
    mcu: str = "esp32"
) -> Dict[str, Any]:
    """Analyzes C++ firmware routines for active vs deep sleep duty cycle current draw."""
    code_lower = cpp_code.lower()
    
    has_wifi = "wifi" in code_lower
    has_ble = "ble" in code_lower or "bluetooth" in code_lower
    has_deep_sleep = "esp_deep_sleep" in code_lower or "deepsleep" in code_lower
    
    # Base active current
    if has_wifi:
        active_ma = 160.0
    elif has_ble:
        active_ma = 80.0
    else:
        active_ma = 40.0
        
    sleep_ma = 0.01 if has_deep_sleep else 15.0
    duty_cycle_pct = 5.0 if has_deep_sleep else 100.0
    
    avg_current_ma = (active_ma * (duty_cycle_pct / 100.0)) + (sleep_ma * ((100.0 - duty_cycle_pct) / 100.0))
    battery_life_hours = battery_mah / avg_current_ma if avg_current_ma > 0 else 0
    battery_life_days = battery_life_hours / 24.0

    return {
        "status": "success",
        "mcu": mcu,
        "active_features": {"wifi": has_wifi, "ble": has_ble, "deep_sleep": has_deep_sleep},
        "active_current_ma": active_ma,
        "sleep_current_ma": sleep_ma,
        "estimated_duty_cycle_pct": duty_cycle_pct,
        "average_current_ma": round(avg_current_ma, 2),
        "estimated_battery_days": round(battery_life_days, 1)
    }
