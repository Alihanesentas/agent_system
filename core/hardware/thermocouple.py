"""
Thermocouple Cold Junction Compensation (CJC) & Type Selector.
Calculates Seebeck coefficient (uV/°C), cold junction temperature compensation,
linearized output voltage (mV), and MAX31855 / MAX31856 IC selection.
"""

from typing import Dict, Any

def design_thermocouple_interface(
    tc_type: str = "K",
    target_temp_c: float = 500.0,
    cold_junction_temp_c: float = 25.0
) -> Dict[str, Any]:
    """
    Calculates thermocouple EMF (mV) and Cold Junction Compensation parameters.
    """
    tc = tc_type.upper().strip()
    
    seebeck_coefficients = {
        "K": 41.2,   # uV/°C
        "J": 50.2,   # uV/°C
        "T": 39.0,   # uV/°C
        "E": 68.0,   # uV/°C
        "N": 38.5,   # uV/°C
    }
    
    alpha_uv_c = seebeck_coefficients.get(tc, 41.2)
    delta_t = target_temp_c - cold_junction_temp_c
    emf_mv = (delta_t * alpha_uv_c) / 1000.0
    
    recommended_ic = f"MAX31855{tc}ASA+ or MAX31856 (Universal SPI Thermocouple Converter)"

    return {
        "status": "success",
        "thermocouple_type": tc,
        "seebeck_coefficient_uv_c": alpha_uv_c,
        "target_temp_c": target_temp_c,
        "cold_junction_temp_c": cold_junction_temp_c,
        "differential_emf_mv": round(emf_mv, 3),
        "recommended_converter_ic": recommended_ic
    }
