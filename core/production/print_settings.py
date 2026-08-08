"""
3D Printer Material Slicer Profile & Parameter Recommender.
Recommends nozzle temperature (°C), bed temperature (°C), print speed (mm/s),
cooling fan speed (%), retraction distance (mm), and enclosure requirements for PLA/ABS/PETG/TPU/Nylon.
"""

from typing import Dict, Any

def recommend_print_settings(
    material: str = "PETG",
    nozzle_diameter_mm: float = 0.4
) -> Dict[str, Any]:
    """
    Recommends optimal 3D slicer parameters per material.
    """
    mat = material.upper().strip()
    
    profiles = {
        "PLA": {"nozzle_c": 210, "bed_c": 60, "speed_mms": 60, "fan_pct": 100, "retraction_mm": 0.8, "enclosure": False},
        "PETG": {"nozzle_c": 240, "bed_c": 75, "speed_mms": 45, "fan_pct": 40, "retraction_mm": 1.2, "enclosure": False},
        "ABS": {"nozzle_c": 250, "bed_c": 100, "speed_mms": 50, "fan_pct": 0, "retraction_mm": 0.8, "enclosure": True},
        "TPU": {"nozzle_c": 225, "bed_c": 50, "speed_mms": 25, "fan_pct": 100, "retraction_mm": 0.0, "enclosure": False},
        "NYLON": {"nozzle_c": 265, "bed_c": 90, "speed_mms": 40, "fan_pct": 20, "retraction_mm": 1.0, "enclosure": True},
    }
    
    cfg = profiles.get(mat, profiles["PETG"])

    return {
        "status": "success",
        "material": mat,
        "nozzle_diameter_mm": nozzle_diameter_mm,
        "recommended_layer_height_mm": round(nozzle_diameter_mm * 0.5, 2),
        "nozzle_temperature_c": cfg["nozzle_c"],
        "bed_temperature_c": cfg["bed_c"],
        "print_speed_mm_s": cfg["speed_mms"],
        "cooling_fan_speed_pct": cfg["fan_pct"],
        "retraction_distance_mm": cfg["retraction_mm"],
        "enclosure_required": cfg["enclosure"]
    }
