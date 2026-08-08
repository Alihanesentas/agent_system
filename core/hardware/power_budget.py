"""
System Power Budget & Current Draw Matrix Calculator.
Summarizes current draw (mA), power dissipation (mW), and total energy consumption
across all ICs and peripherals in active vs sleep states.
"""

from typing import Dict, Any, List

def calculate_power_budget(
    components: List[Dict[str, Any]] = None,
    system_voltage_v: float = 3.3
) -> Dict[str, Any]:
    """
    Calculates total active/sleep power consumption and component breakdown.
    """
    if not components:
        components = [
            {"name": "MCU (ESP32-S3)", "active_ma": 80.0, "sleep_ma": 0.015, "duty_cycle_pct": 10.0},
            {"name": "Wi-Fi Radio TX", "active_ma": 240.0, "sleep_ma": 0.0, "duty_cycle_pct": 2.0},
            {"name": "Sensors (I2C/SPI)", "active_ma": 12.0, "sleep_ma": 0.001, "duty_cycle_pct": 10.0},
            {"name": "Status LEDs", "active_ma": 10.0, "sleep_ma": 0.0, "duty_cycle_pct": 5.0},
        ]
    
    total_active_ma = sum(c.get("active_ma", 0.0) for c in components)
    total_sleep_ma = sum(c.get("sleep_ma", 0.0) for c in components)
    
    avg_ma = 0.0
    for c in components:
        d = c.get("duty_cycle_pct", 10.0) / 100.0
        avg_ma += (c.get("active_ma", 0.0) * d) + (c.get("sleep_ma", 0.0) * (1.0 - d))

    total_active_mw = total_active_ma * system_voltage_v
    avg_power_mw = avg_ma * system_voltage_v

    return {
        "status": "success",
        "system_voltage_v": system_voltage_v,
        "component_count": len(components),
        "peak_active_current_ma": round(total_active_ma, 2),
        "peak_active_power_mw": round(total_active_mw, 2),
        "deep_sleep_current_ma": round(total_sleep_ma, 4),
        "average_current_ma": round(avg_ma, 2),
        "average_power_mw": round(avg_power_mw, 2),
        "components_breakdown": components,
        "recommendation": f"Design 3.3V LDO/SMPS rail for peak >{round(total_active_ma * 1.5, 0)}mA headroom."
    }
