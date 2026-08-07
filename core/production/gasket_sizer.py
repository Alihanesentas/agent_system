"""
3D Enclosure Waterproof O-Ring Gasket Seal Sizer Engine.
Calculates IP67 waterproof rubber O-ring compression gland dimensions, groove width (mm),
and groove depth (mm) for sealed 3D enclosures.
"""

from typing import Dict, Any

def calculate_gasket_groove_dimensions(
    oring_cross_section_mm: float = 1.5
) -> Dict[str, Any]:
    """Calculates IP67 O-ring gland groove dimensions."""
    groove_depth = oring_cross_section_mm * 0.75  # 25% compression
    groove_width = oring_cross_section_mm * 1.25  # 25% side expansion

    return {
        "status": "success",
        "oring_cross_section_mm": oring_cross_section_mm,
        "recommended_groove_depth_mm": round(groove_depth, 2),
        "recommended_groove_width_mm": round(groove_width, 2),
        "target_ip_rating": "IP67 Waterproof"
    }
