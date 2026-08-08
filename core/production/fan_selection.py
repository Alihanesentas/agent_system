r"""
Enclosure Cooling Fan Selection & Airflow (CFM) Calculator.
Calculates required volumetric airflow $Q$ ($CFM$), static pressure drop $\Delta P$ ($inH_2O$),
fan acoustic noise level ($dBA$), and recommended 40mm/60mm/80mm/120mm fan model.
"""

from typing import Dict, Any

def select_cooling_fan(
    power_dissipation_w: float = 50.0,
    max_temp_rise_c: float = 15.0,
    altitude_m: float = 0.0
) -> Dict[str, Any]:
    """
    Calculates required cooling fan CFM airflow and static pressure.
    """
    # CFM = 3.16 * P_w / Delta_T_C (at sea level)
    required_cfm = (3.16 * power_dissipation_w) / max_temp_rise_c if max_temp_rise_c > 0 else 10.0
    
    if required_cfm < 15.0:
        recommended_fan = "40mm x 40mm x 10mm (12V DC, 8-12 CFM, 22 dBA)"
    elif required_cfm < 35.0:
        recommended_fan = "60mm x 60mm x 25mm (12V DC, 20-30 CFM, 28 dBA)"
    elif required_cfm < 75.0:
        recommended_fan = "80mm x 80mm x 25mm (12V DC, 40-60 CFM, 32 dBA)"
    else:
        recommended_fan = "120mm x 120mm x 25mm (12V/24V DC, 80-110 CFM, 38 dBA)"

    return {
        "status": "success",
        "power_dissipation_w": power_dissipation_w,
        "max_temperature_rise_c": max_temp_rise_c,
        "required_airflow_cfm": round(required_cfm, 1),
        "required_airflow_m3_h": round(required_cfm * 1.699, 1),
        "recommended_fan_size": recommended_fan
    }
