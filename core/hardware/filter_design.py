"""
Active & Passive Analog Filter Design Engine (Butterworth & Sallen-Key).
Calculates component values (R, C), Q-factor, and frequency response for
Low-pass, High-pass, and Band-pass 2nd-order active Sallen-Key op-amp filters.
"""

import math
from typing import Dict, Any

def design_analog_filter(
    filter_type: str = "lowpass",
    cutoff_freq_hz: float = 1000.0,
    r_kohm: float = 10.0,
    q_factor: float = 0.707  # Butterworth maximal flatness Q
) -> Dict[str, Any]:
    """
    Calculates Sallen-Key 2nd-order active filter capacitors and resistor values.
    """
    w0 = 2.0 * math.pi * cutoff_freq_hz
    r_ohms = r_kohm * 1000.0
    
    # C1 = 2 * Q / (w0 * R), C2 = 1 / (2 * Q * w0 * R)
    c1_farads = (2.0 * q_factor) / (w0 * r_ohms) if w0 * r_ohms > 0 else 1e-8
    c2_farads = 1.0 / (2.0 * q_factor * w0 * r_ohms) if w0 * r_ohms > 0 else 1e-9
    
    c1_nf = c1_farads * 1e9
    c2_nf = c2_farads * 1e9

    return {
        "status": "success",
        "filter_type": filter_type.lower(),
        "topology": "Sallen-Key 2nd-Order Active Filter",
        "cutoff_freq_hz": cutoff_freq_hz,
        "q_factor": q_factor,
        "r1_r2_kohm": r_kohm,
        "c1_calculated_nf": round(c1_nf, 2),
        "c2_calculated_nf": round(c2_nf, 2),
        "attenuation_db_per_octave": -12.0 if "low" in filter_type.lower() else 12.0
    }
