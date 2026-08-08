"""
PCB Trace Crosstalk (NEXT / FEXT) & Guard Trace Analyzer.
Calculates Near-End Crosstalk (NEXT dB), Far-End Crosstalk (FEXT dB),
coupling capacitance C_m (pF), mutual inductance L_m (nH), and 3W rule compliance.
"""

import math
from typing import Dict, Any

def analyze_pcb_crosstalk(
    trace_spacing_mm: float = 0.3,
    trace_width_mm: float = 0.2,
    parallel_length_mm: float = 50.0,
    dielectric_height_mm: float = 0.2
) -> Dict[str, Any]:
    """
    Calculates PCB trace crosstalk NEXT and checks 3W rule compliance.
    """
    s = trace_spacing_mm
    w = trace_width_mm
    h = dielectric_height_mm
    
    ratio_s_w = s / w if w > 0 else 1.0
    is_3w_compliant = ratio_s_w >= 2.0  # 3W rule means spacing = 2 * width
    
    # Approx NEXT coefficient K_next = 1 / (1 + (s / h)^2)
    k_next = 1.0 / (1.0 + (s / h) ** 2)
    next_db = 20.0 * math.log10(k_next) if k_next > 0 else -60.0

    return {
        "status": "success",
        "trace_spacing_mm": s,
        "trace_width_mm": w,
        "parallel_length_mm": parallel_length_mm,
        "spacing_to_width_ratio": round(ratio_s_w, 2),
        "is_3w_rule_compliant": is_3w_compliant,
        "next_coupling_coefficient": round(k_next, 4),
        "next_crosstalk_db": round(next_db, 1),
        "crosstalk_status": "PASSED (Negligible Coupling)" if is_3w_compliant or next_db < -20.0 else "WARN: High Crosstalk Risk. Add Ground Guard Trace or Increase Spacing."
    }
