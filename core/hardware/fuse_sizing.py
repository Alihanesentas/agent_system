"""
Electric Fuse Sizing & Melting Integral I²t Calculator.
Calculates continuous current fuse rating I_fuse (A), melting integral I²t (A²s),
inrush surge current withstand capability, and PTC resettable fuse selection.
"""

from typing import Dict, Any

def calculate_fuse_sizing(
    normal_current_a: float = 3.0,
    max_ambient_temp_c: float = 60.0,
    inrush_peak_current_a: float = 25.0,
    inrush_duration_ms: float = 5.0
) -> Dict[str, Any]:
    """
    Calculates fuse rating with temperature derating and inrush I²t rating.
    """
    # Temperature derating factor (typical 0.85 at 60°C)
    temp_derating = 0.85 if max_ambient_temp_c >= 50.0 else 1.0
    safety_factor = 1.25
    
    recommended_fuse_rating_a = (normal_current_a * safety_factor) / temp_derating
    
    # Inrush energy I²t = (I_peak^2) * (duration / 2) for triangular inrush
    inrush_i2t = (inrush_peak_current_a ** 2) * (inrush_duration_ms / 2000.0)
    
    # Required fuse I²t = inrush_i2t / pulse_factor (0.3 for 10,000 pulses)
    required_fuse_i2t = inrush_i2t / 0.3

    return {
        "status": "success",
        "normal_operating_current_a": normal_current_a,
        "max_ambient_temp_c": max_ambient_temp_c,
        "temperature_derating_factor": temp_derating,
        "recommended_fuse_rating_a": round(recommended_fuse_rating_a, 2),
        "nearest_standard_fuse_a": round(recommended_fuse_rating_a + 0.5, 0),
        "inrush_pulse_i2t_a2s": round(inrush_i2t, 4),
        "min_required_fuse_i2t_a2s": round(required_fuse_i2t, 4),
        "fuse_type_recommendation": "Slow-Blow / Time-Lag Fuse (T) for inductive/capacitive inrush"
    }
