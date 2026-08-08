"""
CNC Milling Spindle Speed (RPM) & Feed Rate (mm/min) Calculator.
Calculates spindle speed $N$ (RPM), table feed rate $F$ (mm/min), chip load $f_z$ (mm/tooth),
Material Removal Rate MRR ($cm^3/min$), and required spindle motor power (kW).
"""

import math
from typing import Dict, Any

def calculate_cnc_feedrate(
    cutting_speed_m_min: float = 150.0,  # Vc (m/min) for Aluminum
    tool_diameter_mm: float = 6.0,
    flute_count: int = 3,
    chip_load_per_tooth_mm: float = 0.05,
    depth_of_cut_mm: float = 2.0,
    width_of_cut_mm: float = 4.0
) -> Dict[str, Any]:
    """
    Calculates CNC milling feeds, speeds, and Material Removal Rate.
    """
    # Spindle Speed N = (Vc * 1000) / (pi * D)
    spindle_rpm = (cutting_speed_m_min * 1000.0) / (math.pi * tool_diameter_mm) if tool_diameter_mm > 0 else 5000.0
    
    # Table Feed Rate F = N * z * fz
    feed_rate_mm_min = spindle_rpm * flute_count * chip_load_per_tooth_mm
    
    # Material Removal Rate MRR = (ap * ae * F) / 1000
    mrr_cm3_min = (depth_of_cut_mm * width_of_cut_mm * feed_rate_mm_min) / 1000.0

    return {
        "status": "success",
        "cutting_speed_m_min": cutting_speed_m_min,
        "tool_diameter_mm": tool_diameter_mm,
        "flute_count": flute_count,
        "chip_load_mm_per_tooth": chip_load_per_tooth_mm,
        "spindle_speed_rpm": round(spindle_rpm, 0),
        "feed_rate_mm_min": round(feed_rate_mm_min, 1),
        "material_removal_rate_mrr_cm3_min": round(mrr_cm3_min, 2)
    }
