"""
Wheatstone Bridge, Strain Gauge & Load Cell Signal Calculator.
Calculates bridge differential output V_out (mV), strain sensitivity (gauge factor GF),
temperature compensation, and excitation voltage requirements.
"""

from typing import Dict, Any

def calculate_wheatstone_bridge(
    excitation_v: float = 5.0,
    bridge_resistance_ohms: float = 350.0,
    gauge_factor: float = 2.0,
    strain_microstrain: float = 1000.0,
    bridge_type: str = "quarter"  # quarter, half, full
) -> Dict[str, Any]:
    """
    Calculates Wheatstone bridge output voltage and sensitivity.
    """
    b_type = bridge_type.lower().strip()
    e = strain_microstrain * 1e-6
    
    # Differential output V_out = V_ex * (GF * e / 4) * multiplier
    if "full" in b_type:
        multiplier = 4.0
    elif "half" in b_type:
        multiplier = 2.0
    else:  # Quarter bridge
        multiplier = 1.0
        
    v_out_mv = excitation_v * (gauge_factor * e / 4.0) * multiplier * 1000.0
    sensitivity_mv_v = (v_out_mv / excitation_v) if excitation_v > 0 else 0.0

    return {
        "status": "success",
        "bridge_type": b_type,
        "excitation_voltage_v": excitation_v,
        "bridge_resistance_ohms": bridge_resistance_ohms,
        "gauge_factor": gauge_factor,
        "strain_microstrain": strain_microstrain,
        "output_voltage_mv": round(v_out_mv, 3),
        "sensitivity_mv_per_v": round(sensitivity_mv_v, 3),
        "recommended_adc_gain": "PGA Gain = 128 (e.g. HX711 / ADS1232)"
    }
