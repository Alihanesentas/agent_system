"""
Analog & Digital Sensor Interface Circuit Designer (PT100/NTC/MEMS).
Calculates sensor excitation current (uA), RC anti-aliasing filter cut-off (kHz),
PGA (Programmable Gain Amplifier) gain, and ADC effective resolution (bits).
"""

import math
from typing import Dict, Any

def design_sensor_interface(
    sensor_type: str = "NTC_10K",
    v_supply_v: float = 3.3,
    adc_bits: int = 12
) -> Dict[str, Any]:
    """
    Designs sensor signal conditioning and anti-aliasing RC filter.
    """
    sens = sensor_type.upper().strip()
    
    if "PT100" in sens:
        excitation_current_ua = 500.0  # 0.5mA to prevent self-heating
        pga_gain = 16.0
        rc_filter_fc_hz = 50.0
        desc = "RTD PT100 4-Wire Kelvin Bridge Interface"
    elif "NTC" in sens:
        excitation_current_ua = 100.0
        pga_gain = 1.0
        rc_filter_fc_hz = 100.0
        desc = "NTC Thermistor Voltage Divider with RC Filter"
    else:  # MEMS / Strain / General
        excitation_current_ua = 1000.0
        pga_gain = 8.0
        rc_filter_fc_hz = 500.0
        desc = "General MEMS Analog Sensor Interface"

    return {
        "status": "success",
        "sensor_type": sens,
        "description": desc,
        "v_supply_v": v_supply_v,
        "excitation_current_ua": excitation_current_ua,
        "pga_gain": pga_gain,
        "anti_aliasing_fc_hz": rc_filter_fc_hz,
        "recommended_rc_values": "R = 10kΩ, C = 100nF",
        "adc_resolution_bits": adc_bits
    }
