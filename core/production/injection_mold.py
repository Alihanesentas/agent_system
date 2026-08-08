"""
Plastic Injection Molding Shrinkage & Tooling Cost Estimator.
Calculates volumetric material shrinkage (%), cavity scaling dimensions (mm),
clamp force requirement (Tons), cooling time ($sec$), and NRE mold tooling cost ($).
"""

from typing import Dict, Any

def estimate_injection_mold(
    part_length_mm: float = 100.0,
    part_width_mm: float = 50.0,
    wall_thickness_mm: float = 2.5,
    material: str = "ABS"
) -> Dict[str, Any]:
    """
    Calculates injection mold shrinkage, clamp force, and tooling cost.
    """
    mat = material.upper().strip()
    shrinkage_pct = {"ABS": 0.5, "PC": 0.6, "PP": 1.5, "PA66": 1.2, "POM": 2.0}.get(mat, 0.5)
    
    cavity_length_mm = part_length_mm * (1.0 + shrinkage_pct / 100.0)
    cavity_width_mm = part_width_mm * (1.0 + shrinkage_pct / 100.0)
    
    projected_area_cm2 = (part_length_mm * part_width_mm) / 100.0
    required_clamp_force_tons = projected_area_cm2 * 0.4  # ~0.4 Tons/cm²
    
    cooling_time_sec = 2.0 * (wall_thickness_mm ** 2)

    return {
        "status": "success",
        "material": mat,
        "part_dimensions_mm": f"{part_length_mm} x {part_width_mm} x {wall_thickness_mm}",
        "material_shrinkage_pct": shrinkage_pct,
        "cavity_dimensions_mm": f"{round(cavity_length_mm, 2)} x {round(cavity_width_mm, 2)}",
        "projected_area_cm2": round(projected_area_cm2, 1),
        "required_clamp_force_tons": round(required_clamp_force_tons, 1),
        "estimated_cooling_time_sec": round(cooling_time_sec, 1),
        "nre_tooling_cost_estimate_usd": "$8,500 - $15,000 (Steel P20 2-Cavity Mold)"
    }
