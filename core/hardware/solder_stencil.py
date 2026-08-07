"""
PCB Surface Mount Solder Paste Stencil Area Calculator Engine.
Calculates total SMT pad surface area (mm2), solder paste volume (mm3),
and stainless steel stencil foil thickness (100um / 120um / 150um).
"""

from typing import Dict, Any

def calculate_solder_stencil_specs(
    smt_pad_count: int = 140,
    smallest_pitch_mm: float = 0.5
) -> Dict[str, Any]:
    """Calculates SMT stencil foil thickness and aperture reduction ratio."""
    if smallest_pitch_mm <= 0.4:
        foil_um = 100
    elif smallest_pitch_mm <= 0.5:
        foil_um = 120
    else:
        foil_um = 150

    est_paste_volume_mm3 = smt_pad_count * 0.15 * (foil_um / 100.0)

    return {
        "status": "success",
        "total_smt_pads": smt_pad_count,
        "smallest_component_pitch_mm": smallest_pitch_mm,
        "recommended_stencil_foil_um": foil_um,
        "aperture_reduction_pct": 10.0,
        "estimated_paste_volume_mm3": round(est_paste_volume_mm3, 2)
    }
