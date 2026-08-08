"""
Electromechanical Solenoid Actuator Force & Flyback Diode Designer.
Calculates solenoid magnetic holding force $F$ ($N$), coil inductance $L$ ($mH$),
operating current $I$ ($A$), coil heating power ($W$), and flyback TVS diode ratings.
"""

import math
from typing import Dict, Any

def design_solenoid(
    coil_turns: int = 500,
    voltage_v: float = 12.0,
    coil_resistance_ohms: float = 10.0,
    plunger_gap_mm: float = 2.0
) -> Dict[str, Any]:
    """
    Calculates solenoid electromagnetic force and coil power loss.
    """
    current_a = voltage_v / coil_resistance_ohms if coil_resistance_ohms > 0 else 1.0
    power_w = voltage_v * current_a
    
    gap_m = plunger_gap_mm / 1000.0
    mu0 = 4.0 * math.pi * 1e-7
    area_m2 = math.pi * ((0.005) ** 2)  # 10mm plunger diameter
    
    # Approx Force F = (N * I)^2 * mu0 * A / (2 * g^2)
    force_n = (((coil_turns * current_a) ** 2) * mu0 * area_m2) / (2.0 * (gap_m ** 2)) if gap_m > 0 else 5.0
    
    flyback_diode_current_a = current_a * 1.5
    flyback_diode_voltage_v = voltage_v * 3.0

    return {
        "status": "success",
        "coil_turns": coil_turns,
        "operating_voltage_v": voltage_v,
        "coil_current_a": round(current_a, 2),
        "coil_power_w": round(power_w, 2),
        "plunger_air_gap_mm": plunger_gap_mm,
        "electromagnetic_force_n": round(force_n, 2),
        "electromagnetic_force_kgf": round(force_n / 9.81, 2),
        "recommended_flyback_diode": f"1N4007 or TVS Diode (I >= {round(flyback_diode_current_a, 1)}A, VRRM >= {round(flyback_diode_voltage_v, 0)}V)"
    }
