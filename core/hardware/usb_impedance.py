"""
USB 2.0 / USB 3.0 Differential Impedance Checker (90Ω Z_diff).
Calculates D+/D- differential microstrip impedance Z_diff (Ω), trace width w (mm),
pair spacing s (mm), and USB 2.0 High-Speed / USB 3.2 Gen 2 signal integrity compliance.
"""

import math
from typing import Dict, Any

def check_usb_impedance(
    trace_width_mm: float = 0.2,
    pair_spacing_mm: float = 0.15,
    substrate_height_mm: float = 0.2,
    er_dielectric: float = 4.2  # FR-4
) -> Dict[str, Any]:
    """
    Calculates USB 90Ω differential pair impedance.
    """
    w = trace_width_mm
    s = pair_spacing_mm
    h = substrate_height_mm
    
    # Single-ended microstrip impedance Z0
    z0 = (87.0 / math.sqrt(er_dielectric + 1.41)) * math.log((5.98 * h) / (0.8 * w + 0.001))
    
    # Differential impedance Z_diff = 2 * Z0 * (1 - 0.48 * exp(-0.96 * (s / h)))
    z_diff = 2.0 * z0 * (1.0 - 0.48 * math.exp(-0.96 * (s / h)))
    
    target_z_diff = 90.0
    error_pct = abs((z_diff - target_z_diff) / target_z_diff) * 100.0

    return {
        "status": "success",
        "trace_width_mm": w,
        "pair_spacing_mm": s,
        "substrate_height_mm": h,
        "dielectric_er": er_dielectric,
        "single_ended_z0_ohms": round(z0, 1),
        "calculated_z_diff_ohms": round(z_diff, 1),
        "target_z_diff_ohms": target_z_diff,
        "impedance_error_pct": round(error_pct, 2),
        "usb_compliance": "PASSED (90Ω ± 10% Compliant)" if error_pct <= 10.0 else "WARN: Differential impedance deviates from 90Ω target"
    }
