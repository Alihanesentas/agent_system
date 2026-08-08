"""
Tolerance Stack-Up Analysis Engine (Worst-Case & RSS).
Calculates Worst-Case max/min gap dimensions and Root-Sum-Square (RSS) 3-sigma statistical distribution
tolerances for precision mechanical 3D assemblies and CNC machined parts.
"""

import math
from typing import Dict, Any, List

def analyze_tolerance_stack(
    dimensions_mm: List[float] = [50.0, -20.0, -29.5],
    tolerances_mm: List[float] = [0.1, 0.05, 0.05]
) -> Dict[str, Any]:
    """
    Calculates Worst-Case and Root-Sum-Square (RSS) statistical tolerance limits.
    """
    nominal_gap = sum(dimensions_mm)
    
    worst_case_tolerance = sum(abs(t) for t in tolerances_mm)
    worst_case_max = nominal_gap + worst_case_tolerance
    worst_case_min = nominal_gap - worst_case_tolerance
    
    # RSS statistical tolerance = sqrt(sum(t_i^2))
    rss_tolerance = math.sqrt(sum(t**2 for t in tolerances_mm))
    rss_max = nominal_gap + rss_tolerance
    rss_min = nominal_gap - rss_tolerance

    return {
        "status": "success",
        "dimension_count": len(dimensions_mm),
        "nominal_gap_mm": round(nominal_gap, 3),
        "worst_case": {
            "tolerance_mm": round(worst_case_tolerance, 3),
            "max_gap_mm": round(worst_case_max, 3),
            "min_gap_mm": round(worst_case_min, 3)
        },
        "rss_3sigma_statistical": {
            "tolerance_mm": round(rss_tolerance, 3),
            "max_gap_mm": round(rss_max, 3),
            "min_gap_mm": round(rss_min, 3)
        },
        "assembly_fit": "INTERFERENCE RISK" if worst_case_min < 0 else "CLEARANCE FIT"
    }
