"""
KiCad PCB Trace Differential Pair Skew & Length Matching Calculator Engine.
Calculates high-speed differential pair length matching (USB 2.0 / Ethernet / CAN)
and serpentine tuning wave counts to prevent phase skew.
"""

from typing import Dict, Any

def calculate_length_matching(
    trace_a_len_mm: float = 42.50,
    trace_b_len_mm: float = 42.15,
    max_skew_mm: float = 0.15
) -> Dict[str, Any]:
    """Calculates length mismatch and required serpentine tuning waves."""
    mismatch_mm = abs(trace_a_len_mm - trace_b_len_mm)
    in_spec = mismatch_mm <= max_skew_mm
    needed_serpentines = max(0, int(round((mismatch_mm / 0.5))))

    return {
        "status": "success",
        "trace_a_len_mm": trace_a_len_mm,
        "trace_b_len_mm": trace_b_len_mm,
        "mismatch_mm": round(mismatch_mm, 3),
        "max_allowable_skew_mm": max_skew_mm,
        "length_matching_status": "MATCHED" if in_spec else "SKEW_WARNING",
        "recommended_serpentine_waves": needed_serpentines
    }
