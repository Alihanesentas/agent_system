"""
PCB Via Current Capacity & Thermal Via Array Calculator (IPC-2152).
Calculates maximum DC current (A), DC resistance (mΩ), voltage drop (mV),
and thermal dissipation rating (°C rise) for PCB vias and thermal via matrix arrays.
"""

import math
from typing import Dict, Any

def calculate_via_current(
    drill_diameter_mm: float = 0.3,
    plating_thickness_um: float = 25.0,
    board_thickness_mm: float = 1.6,
    temp_rise_c: float = 10.0
) -> Dict[str, Any]:
    """
    Calculates via current carrying capacity and via array matrix requirements.
    """
    # Plating cross-sectional area A (mil^2)
    # Outer diameter d, inner diameter = d - 2*t
    d_mil = drill_diameter_mm * 39.3701
    t_mil = (plating_thickness_um / 1000.0) * 39.3701
    
    cross_section_mil2 = math.pi * ((d_mil / 2.0)**2 - ((d_mil - 2.0*t_mil) / 2.0)**2)
    
    # IPC-2152 Current formula I = k * (dT)^b * (A)^c
    # For internal/external via approximation: k=0.048, b=0.44, c=0.725
    max_current_a = 0.048 * (temp_rise_c ** 0.44) * (cross_section_mil2 ** 0.725)
    
    # Via DC Resistance R = rho * L / A
    rho_copper = 1.7e-8  # Ohm-meter
    l_m = board_thickness_mm / 1000.0
    a_m2 = cross_section_mil2 * 6.4516e-10
    
    r_via_mohm = (rho_copper * l_m / a_m2) * 1000.0
    v_drop_mv = max_current_a * (r_via_mohm / 1000.0) * 1000.0

    return {
        "status": "success",
        "drill_diameter_mm": drill_diameter_mm,
        "plating_thickness_um": plating_thickness_um,
        "board_thickness_mm": board_thickness_mm,
        "temp_rise_target_c": temp_rise_c,
        "max_current_per_via_a": round(max_current_a, 2),
        "via_dc_resistance_mohm": round(r_via_mohm, 2),
        "voltage_drop_at_max_current_mv": round(v_drop_mv, 2),
        "thermal_matrix_guide": {
            "for_10A_rail": f"Use minimum {math.ceil(10.0 / max_current_a)} vias in parallel",
            "for_20A_rail": f"Use minimum {math.ceil(20.0 / max_current_a)} vias in parallel"
        }
    }
