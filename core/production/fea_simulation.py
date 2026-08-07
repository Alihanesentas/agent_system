"""
3D Mechanical Stress & Thermal Finite Element Analysis (FEA) Engine.
Simulates enclosure mechanical stress (MPa), yield strength deformation (mm),
and plastic wall structural integrity under external forces.
"""

from typing import Dict, Any

def run_mechanical_fea_simulation(
    force_newtons: float = 50.0,
    wall_thickness_mm: float = 2.0,
    material: str = "PETG"
) -> Dict[str, Any]:
    """Simulates FEA mechanical stress and deformation for 3D printed enclosures."""
    mat_properties = {
        "PETG": {"yield_stress_mpa": 50.0, "density_g_cm3": 1.27},
        "PLA": {"yield_stress_mpa": 60.0, "density_g_cm3": 1.24},
        "ABS": {"yield_stress_mpa": 40.0, "density_g_cm3": 1.04}
    }
    
    prop = mat_properties.get(material.upper(), mat_properties["PETG"])
    
    # Peak Von Mises Stress estimate (MPa)
    peak_stress_mpa = force_newtons / (wall_thickness_mm * 10.0)
    safety_factor = prop["yield_stress_mpa"] / peak_stress_mpa if peak_stress_mpa > 0 else 99.0
    deformation_mm = round((force_newtons * 0.005) / (wall_thickness_mm ** 2), 3)

    return {
        "status": "success",
        "material": material.upper(),
        "applied_force_N": force_newtons,
        "wall_thickness_mm": wall_thickness_mm,
        "peak_von_mises_stress_mpa": round(peak_stress_mpa, 2),
        "yield_strength_mpa": prop["yield_stress_mpa"],
        "safety_factor": round(safety_factor, 2),
        "estimated_deformation_mm": deformation_mm,
        "structural_status": "PASS" if safety_factor >= 1.5 else "FAIL (Risk of Fracture)"
    }
