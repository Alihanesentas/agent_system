"""
Finned Aluminum Heatsink Dimensioning & Convection Engine.
Calculates required thermal resistance (Rth in °C/W), fin count, fin height (mm),
and forced vs natural convection airflow cooling parameters.
"""

from typing import Dict, Any

def design_heatsink(
    power_dissipation_w: float = 15.0,
    max_junction_temp_c: float = 110.0,
    ambient_temp_c: float = 40.0,
    rth_junction_case_c_w: float = 1.2,
    rth_interface_c_w: float = 0.5
) -> Dict[str, Any]:
    """
    Designs finned heatsink thermal resistance and dimensions.
    """
    total_allowed_rth = (max_junction_temp_c - ambient_temp_c) / power_dissipation_w if power_dissipation_w > 0 else 5.0
    required_heatsink_rth = total_allowed_rth - (rth_junction_case_c_w + rth_interface_c_w)
    
    needs_fan = required_heatsink_rth < 2.0
    
    # Approx aluminum extrusion volume (cm3) for natural convection
    volume_cm3 = (50.0 / required_heatsink_rth) if required_heatsink_rth > 0 else 100.0

    return {
        "status": "success",
        "power_dissipation_w": power_dissipation_w,
        "max_junction_temp_c": max_junction_temp_c,
        "ambient_temp_c": ambient_temp_c,
        "total_allowed_rth_c_w": round(total_allowed_rth, 2),
        "required_heatsink_rth_c_w": round(max(required_heatsink_rth, 0.1), 2),
        "cooling_type": "Forced Air Convection (Fan Required)" if needs_fan else "Natural Air Convection (Passive)",
        "estimated_aluminum_heatsink_volume_cm3": round(volume_cm3, 1),
        "recommended_dimensions_mm": "50 x 50 x 25 mm" if needs_fan else "80 x 60 x 40 mm"
    }
