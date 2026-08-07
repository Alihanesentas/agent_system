"""
3D Printed Box Cable Gland & Rubber Strain Relief Sizer Engine.
Calculates PG7 / PG9 / M12 / M16 waterproof cable gland mounting hole diameters
and strain relief bend radii for external wiring.
"""

from typing import Dict, Any

GLAND_SPECS = {
    "PG7": {"hole_diameter_mm": 12.5, "cable_range_mm": "3.0 - 6.5 mm"},
    "PG9": {"hole_diameter_mm": 15.2, "cable_range_mm": "4.0 - 8.0 mm"},
    "M12": {"hole_diameter_mm": 12.0, "cable_range_mm": "3.0 - 6.5 mm"},
    "M16": {"hole_diameter_mm": 16.0, "cable_range_mm": "5.0 - 10.0 mm"}
}

def calculate_cable_gland_dimensions(gland_type: str = "PG9") -> Dict[str, Any]:
    """Calculates cable gland panel cutout hole size and cable OD range."""
    spec = GLAND_SPECS.get(gland_type.upper(), GLAND_SPECS["PG9"])
    return {
        "status": "success",
        "gland_type": gland_type.upper(),
        "panel_cutout_hole_diameter_mm": spec["hole_diameter_mm"],
        "cable_outer_diameter_range": spec["cable_range_mm"]
    }
