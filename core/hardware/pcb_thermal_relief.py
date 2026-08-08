r"""
PCB Thermal Relief Pad Pattern & Spoke Width Calculator.
Calculates thermal spoke width (mm), number of spokes (2-4), spoke copper cross-sectional area,
and soldering thermal resistance ($^\circ C/W$) for SMD/PTH pads connected to ground planes.
"""

from typing import Dict, Any

def calculate_thermal_relief(
    pad_diameter_mm: float = 1.6,
    hole_diameter_mm: float = 0.8,
    spoke_count: int = 4,
    spoke_width_mm: float = 0.3,
    copper_thickness_oz: float = 1.0
) -> Dict[str, Any]:
    """
    Calculates PCB thermal relief spoke pattern for wave/reflow soldering.
    """
    copper_thickness_mm = copper_thickness_oz * 0.035
    total_spoke_width_mm = spoke_count * spoke_width_mm
    
    cross_sectional_area_mm2 = total_spoke_width_mm * copper_thickness_mm
    
    # Thermal resistance R_th = L / (k * A)
    thermal_resistance_c_w = 0.5 / (400.0 * cross_sectional_area_mm2 * 1e-6) if cross_sectional_area_mm2 > 0 else 100.0

    return {
        "status": "success",
        "pad_diameter_mm": pad_diameter_mm,
        "hole_diameter_mm": hole_diameter_mm,
        "spoke_count": spoke_count,
        "spoke_width_mm": spoke_width_mm,
        "copper_thickness_oz": copper_thickness_oz,
        "total_spoke_copper_area_mm2": round(cross_sectional_area_mm2, 4),
        "thermal_resistance_c_w": round(thermal_resistance_c_w, 2),
        "solderability_verdict": "GOOD (Easy Reflow/Wave Soldering)" if thermal_resistance_c_w > 1.0 else "WARN: High Copper Heat Sinking. Soldering Cold Joint Risk."
    }
