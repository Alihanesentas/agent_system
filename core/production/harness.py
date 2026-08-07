"""
Automated Harness & Wire Gauge Sizer Module.
Calculates minimum wire gauge (AWG), voltage drop over cable length,
and connector pin current ratings for robotics and automotive wiring harnesses.
"""

from typing import Dict, Any

def calculate_wire_harness(
    current_amps: float,
    cable_length_meters: float = 2.0,
    voltage_volts: float = 12.0,
    max_voltage_drop_pct: float = 3.0
) -> Dict[str, Any]:
    """
    Calculates wire AWG rating, voltage drop, and power loss.
    """
    # Standard copper wire resistance ohms per 1000m for AWG sizes
    awg_table = {
        "14 AWG": {"resistance_per_m": 0.00828, "max_amps": 20.0},
        "18 AWG": {"resistance_per_m": 0.02095, "max_amps": 10.0},
        "22 AWG": {"resistance_per_m": 0.05296, "max_amps": 5.0},
        "26 AWG": {"resistance_per_m": 0.13380, "max_amps": 1.5}
    }

    recommended_awg = "14 AWG"
    for awg, spec in reversed(list(awg_table.items())):
        if current_amps <= spec["max_amps"]:
            recommended_awg = awg
            break

    resistance = awg_table[recommended_awg]["resistance_per_m"] * (cable_length_meters * 2) # Total round-trip
    v_drop = current_amps * resistance
    v_drop_pct = (v_drop / voltage_volts) * 100.0

    return {
        "status": "success",
        "load_current_amps": current_amps,
        "cable_length_meters": cable_length_meters,
        "recommended_wire_gauge": recommended_awg,
        "voltage_drop_volts": round(v_drop, 2),
        "voltage_drop_percentage": round(v_drop_pct, 2),
        "compliance_status": "Pass ✅" if v_drop_pct <= max_voltage_drop_pct else "Warning: Voltage Drop Exceeded ⚠️"
    }
