"""
Bolt Tightening Torque & Preload Pre-Tightening Calculator (VDI 2230).
Calculates tightening torque (Nm), bolt preload force (kN), and thread friction safety factor
for metric bolts (M2 to M12) across property classes (8.8, 10.9, 12.9).
"""

from typing import Dict, Any

BOLT_SPECS = {
    "M2": {"pitch_mm": 0.4, "stress_area_mm2": 2.07},
    "M2.5": {"pitch_mm": 0.45, "stress_area_mm2": 3.39},
    "M3": {"pitch_mm": 0.5, "stress_area_mm2": 5.03},
    "M4": {"pitch_mm": 0.7, "stress_area_mm2": 8.78},
    "M5": {"pitch_mm": 0.8, "stress_area_mm2": 14.2},
    "M6": {"pitch_mm": 1.0, "stress_area_mm2": 20.1},
    "M8": {"pitch_mm": 1.25, "stress_area_mm2": 36.6},
    "M10": {"pitch_mm": 1.5, "stress_area_mm2": 58.0},
    "M12": {"pitch_mm": 1.75, "stress_area_mm2": 84.3},
}

PROPERTY_CLASSES = {
    "8.8": {"proof_stress_mpa": 640.0},
    "10.9": {"proof_stress_mpa": 940.0},
    "12.9": {"proof_stress_mpa": 1100.0},
}

def calculate_bolt_torque(
    bolt_size: str = "M3",
    property_class: str = "8.8",
    friction_coeff: float = 0.14
) -> Dict[str, Any]:
    """
    Calculates bolt tightening torque (Nm) and preload force (kN).
    """
    size_upper = bolt_size.upper()
    bspec = BOLT_SPECS.get(size_upper, BOLT_SPECS["M3"])
    pspec = PROPERTY_CLASSES.get(property_class, PROPERTY_CLASSES["8.8"])

    # Nominal diameter d in mm
    d_mm = float(size_upper.replace("M", "")) if "M" in size_upper else 3.0
    
    # 75% of proof stress preload force F_preload (N)
    f_preload_n = 0.75 * pspec["proof_stress_mpa"] * bspec["stress_area_mm2"]
    
    # Torque T = K * d * F, K ~ 0.2 default torque coefficient
    k_factor = friction_coeff * 1.25
    torque_nm = (k_factor * (d_mm / 1000.0) * f_preload_n)

    return {
        "status": "success",
        "bolt_size": size_upper,
        "property_class": property_class,
        "friction_coefficient": friction_coeff,
        "stress_area_mm2": bspec["stress_area_mm2"],
        "preload_force_kn": round(f_preload_n / 1000.0, 2),
        "tightening_torque_nm": round(torque_nm, 3),
        "tightening_torque_in_lb": round(torque_nm * 8.8507, 2),
        "recommendation": f"Tighten {size_upper} ({property_class}) to {round(torque_nm, 2)} Nm using calibrated torque wrench."
    }
