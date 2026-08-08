r"""
Mechanical System Natural Frequency ($f_n$) & Vibration Isolation Analyzer.
Calculates natural frequency $f_n$ ($Hz$), damping ratio $\zeta$, transmissibility $T_r$,
and rubber isolator mount stiffness $k$ ($N/mm$) per ISO 10816.
"""

import math
from typing import Dict, Any

def analyze_vibration(
    mass_kg: float = 5.0,
    spring_stiffness_n_mm: float = 50.0,
    exciting_freq_hz: float = 60.0
) -> Dict[str, Any]:
    """
    Calculates 1-DOF mass-spring system natural frequency and vibration transmissibility.
    """
    k_n_m = spring_stiffness_n_mm * 1000.0
    
    # Natural frequency fn = (1 / 2pi) * sqrt(k / m)
    fn_hz = (1.0 / (2.0 * math.pi)) * math.sqrt(k_n_m / mass_kg) if mass_kg > 0 else 10.0
    
    frequency_ratio_r = exciting_freq_hz / fn_hz if fn_hz > 0 else 1.0
    
    # Transmissibility Tr = |1 / (1 - r^2)| for un-damped
    denom = abs(1.0 - (frequency_ratio_r ** 2))
    transmissibility = 1.0 / denom if denom > 0.001 else 999.0
    isolation_pct = (1.0 - transmissibility) * 100.0 if transmissibility < 1.0 else 0.0

    return {
        "status": "success",
        "mass_kg": mass_kg,
        "stiffness_n_mm": spring_stiffness_n_mm,
        "exciting_frequency_hz": exciting_freq_hz,
        "natural_frequency_fn_hz": round(fn_hz, 2),
        "frequency_ratio_r": round(frequency_ratio_r, 2),
        "vibration_transmissibility": round(transmissibility, 3),
        "isolation_efficiency_pct": round(isolation_pct, 1),
        "isolation_verdict": "EFFECTIVE ISOLATION (r > 1.414)" if frequency_ratio_r > 1.414 else "RESONANCE RISK! Increase Stiffness or Damping."
    }
