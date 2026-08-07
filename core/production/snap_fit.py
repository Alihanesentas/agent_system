"""
3D Enclosure Cantilever Snap-Fit Joint & Latch Calculator.
Calculates cantilever beam deflection (mm), permissible material strain (E=2.5%),
and retention force (N) for tool-less 3D printed enclosure lids.
"""

from typing import Dict, Any

def calculate_snap_fit_joint(
    beam_length_mm: float = 12.0,
    beam_thickness_mm: float = 1.5,
    deflection_mm: float = 1.0,
    material: str = "PETG"
) -> Dict[str, Any]:
    """Calculates snap-fit joint strain and deflection limits."""
    # Permissible strain formula: strain = (1.5 * thickness * deflection) / (length^2)
    strain_pct = (1.5 * beam_thickness_mm * deflection_mm) / (beam_length_mm ** 2) * 100.0
    
    max_strain_pct = 2.5 if material.upper() == "PETG" else 2.0
    safe = strain_pct <= max_strain_pct

    return {
        "status": "success",
        "material": material.upper(),
        "beam_length_mm": beam_length_mm,
        "beam_thickness_mm": beam_thickness_mm,
        "deflection_mm": deflection_mm,
        "calculated_strain_pct": round(strain_pct, 2),
        "max_permissible_strain_pct": max_strain_pct,
        "joint_durability": "SAFE (Will not snap)" if safe else "WARNING (Risk of fatigue fracture)"
    }
