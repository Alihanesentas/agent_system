r"""
Linear Actuator & Lead Screw / Ball Screw Sizer.
Calculates required thrust force $F$ ($N$), lead screw pitch ($mm$), motor drive torque $\tau$ ($N\cdot m$),
linear travel speed ($mm/s$), and ball screw mechanical efficiency (%).
"""

import math
from typing import Dict, Any

def select_linear_actuator(
    target_load_kg: float = 20.0,
    travel_speed_mm_s: float = 10.0,
    stroke_length_mm: float = 150.0,
    screw_type: str = "ball_screw"  # ball_screw, lead_screw
) -> Dict[str, Any]:
    """
    Calculates lead/ball screw drive torque and motor power.
    """
    load_n = target_load_kg * 9.81
    screw = screw_type.lower().strip()
    
    if "ball" in screw:
        efficiency = 0.90
        pitch_mm = 5.0
        desc = "High-Precision Ball Screw SFU1205"
    else:
        efficiency = 0.40
        pitch_mm = 2.0
        desc = "Trapezoidal Lead Screw T8x2"
        
    lead_m = pitch_mm / 1000.0
    
    # Motor Torque T = (F * P) / (2 * pi * eta)
    torque_nm = (load_n * lead_m) / (2.0 * math.pi * efficiency)
    
    screw_rpm = (travel_speed_mm_s / pitch_mm) * 60.0 if pitch_mm > 0 else 300.0
    power_w = (torque_nm * (2.0 * math.pi * screw_rpm / 60.0))

    return {
        "status": "success",
        "target_load_kg": target_load_kg,
        "load_force_n": round(load_n, 1),
        "screw_type": desc,
        "screw_pitch_mm": pitch_mm,
        "efficiency_pct": round(efficiency * 100.0, 1),
        "required_motor_torque_nm": round(torque_nm, 3),
        "screw_speed_rpm": round(screw_rpm, 0),
        "mechanical_power_w": round(power_w, 2),
        "stroke_length_mm": stroke_length_mm
    }
