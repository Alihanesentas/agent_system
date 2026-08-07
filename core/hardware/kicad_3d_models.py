"""
KiCad 3D STEP / WRL Model Placer & Collision Detector Engine.
Maps KiCad footprint packages (QFN-56, SOT-23, 0805, LQFP-64) to 3D STEP model files
and calculates 3D height clearance against enclosure walls.
"""

from typing import Dict, Any, List

FOOTPRINT_3D_CATALOG = {
    "SOT-23-5": {"height_mm": 1.45, "step_model": "SOT-23-5.step", "clearance_needed_mm": 2.0},
    "SOT-223": {"height_mm": 1.80, "step_model": "SOT-223.step", "clearance_needed_mm": 2.5},
    "QFN-56": {"height_mm": 0.90, "step_model": "QFN-56_7x7mm.step", "clearance_needed_mm": 1.5},
    "LQFP-64": {"height_mm": 1.60, "step_model": "LQFP-64_10x10mm.step", "clearance_needed_mm": 2.2},
    "0805": {"height_mm": 0.60, "step_model": "C_0805_2012Metric.step", "clearance_needed_mm": 1.0},
    "0603": {"height_mm": 0.45, "step_model": "C_0603_1608Metric.step", "clearance_needed_mm": 0.8}
}

def analyze_3d_component_clearance(
    footprints: List[str],
    enclosure_height_mm: float = 20.0
) -> Dict[str, Any]:
    """Calculates peak component 3D height and enclosure clearance safety margin."""
    max_height = 0.0
    tallest_component = "None"
    component_details = []

    for fp in footprints:
        info = FOOTPRINT_3D_CATALOG.get(fp, {"height_mm": 1.0, "step_model": f"{fp}.step", "clearance_needed_mm": 1.5})
        component_details.append({"footprint": fp, "height_mm": info["height_mm"], "step_model": info["step_model"]})
        if info["height_mm"] > max_height:
            max_height = info["height_mm"]
            tallest_component = fp

    remaining_clearance = enclosure_height_mm - max_height
    safe = remaining_clearance >= 3.0

    return {
        "status": "success",
        "enclosure_height_mm": enclosure_height_mm,
        "tallest_component": tallest_component,
        "max_component_height_mm": max_height,
        "remaining_clearance_mm": round(remaining_clearance, 2),
        "clearance_safety": "SAFE" if safe else "WARNING (Tight Lid)",
        "components_mapped": component_details
    }
