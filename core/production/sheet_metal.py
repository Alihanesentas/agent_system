"""
Sheet Metal Bend Allowance & K-Factor Flat Pattern Calculator.
Calculates Bend Allowance (BA in mm), Bend Deduction (BD in mm), K-Factor,
and flat pattern unbent blank length for sheet metal fabrication (aluminum/steel).
"""

import math
from typing import Dict, Any

def calculate_sheet_metal_bend(
    sheet_thickness_mm: float = 1.5,
    bend_radius_mm: float = 2.0,
    bend_angle_deg: float = 90.0,
    k_factor: float = 0.33  # Standard air bending
) -> Dict[str, Any]:
    """
    Calculates sheet metal bend allowance and flat pattern length.
    """
    t = sheet_thickness_mm
    r = bend_radius_mm
    a_rad = math.radians(bend_angle_deg)
    
    # Bend Allowance BA = A_rad * (R + K * T)
    ba_mm = a_rad * (r + k_factor * t)
    
    # Setback OSSB = tan(A/2) * (R + T)
    ossb_mm = math.tan(a_rad / 2.0) * (r + t)
    
    # Bend Deduction BD = 2 * OSSB - BA
    bd_mm = 2.0 * ossb_mm - ba_mm

    return {
        "status": "success",
        "sheet_thickness_mm": t,
        "bend_radius_mm": r,
        "bend_angle_deg": bend_angle_deg,
        "k_factor": k_factor,
        "bend_allowance_mm": round(ba_mm, 3),
        "outside_setback_mm": round(ossb_mm, 3),
        "bend_deduction_mm": round(bd_mm, 3),
        "flat_pattern_formula": f"Flat Length = (Flange_1 + Flange_2) - {round(bd_mm, 3)} mm"
    }
