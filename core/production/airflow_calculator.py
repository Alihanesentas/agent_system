"""
3D Enclosure Ventilation Airflow & Thermal Slot Calculator.
Calculates required passive convection slot area (mm2) and forced CFM fan specs
based on internal power dissipation (Watts) and ambient delta T.
"""

from typing import Dict, Any

def calculate_enclosure_ventilation(
    heat_dissipation_watts: float = 5.0,
    max_temp_rise_c: float = 15.0
) -> Dict[str, Any]:
    """Calculates required CFM airflow and passive vent slot surface area."""
    # Airflow CFM formula: CFM = 3.16 * Watts / Delta_T
    cfm_required = (3.16 * heat_dissipation_watts) / max_temp_rise_c
    passive_slot_area_mm2 = heat_dissipation_watts * 120.0
    fan_recommended = cfm_required > 2.0

    return {
        "status": "success",
        "heat_dissipation_watts": heat_dissipation_watts,
        "max_temp_rise_c": max_temp_rise_c,
        "required_airflow_cfm": round(cfm_required, 2),
        "recommended_passive_slot_area_mm2": round(passive_slot_area_mm2, 1),
        "cooling_type": "Active Fan Cooling (40mm 5V Fan)" if fan_recommended else "Passive Natural Convection Vents"
    }
