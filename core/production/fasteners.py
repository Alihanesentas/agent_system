"""
3D Enclosure Fastener & Screw Boss Thread Sizer Engine.
Calculates self-tapping metric screw pilot hole sizes (M2, M2.5, M3, M4) for 3D printed PETG/PLA
screw bosses to prevent thread stripping.
"""

from typing import Dict, Any

FASTENER_SPECS = {
    "M2": {"screw_od_mm": 2.0, "pilot_hole_mm": 1.7, "outer_boss_od_mm": 4.0},
    "M2.5": {"screw_od_mm": 2.5, "pilot_hole_mm": 2.1, "outer_boss_od_mm": 5.0},
    "M3": {"screw_od_mm": 3.0, "pilot_hole_mm": 2.5, "outer_boss_od_mm": 6.0},
    "M4": {"screw_od_mm": 4.0, "pilot_hole_mm": 3.4, "outer_boss_od_mm": 8.0}
}

def calculate_screw_boss_dimensions(screw_type: str = "M3") -> Dict[str, Any]:
    """Calculates 3D printed boss pilot hole diameter and outer wall thickness."""
    spec = FASTENER_SPECS.get(screw_type.upper(), FASTENER_SPECS["M3"])
    return {
        "status": "success",
        "screw_type": screw_type.upper(),
        "screw_outer_diameter_mm": spec["screw_od_mm"],
        "recommended_pilot_hole_mm": spec["pilot_hole_mm"],
        "recommended_boss_od_mm": spec["outer_boss_od_mm"]
    }
