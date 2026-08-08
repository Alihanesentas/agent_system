r"""
Rotary & Linear Optical / Magnetic Encoder Resolution Calculator.
Calculates Pulses Per Revolution (PPR), Quadrature CPR ($4 \times PPR$), linear position resolution ($\mu m$),
max pulse frequency ($kHz$), and position measurement error (arcsec).
"""

from typing import Dict, Any

def calculate_encoder_resolution(
    ppr: int = 1000,
    max_rpm: float = 3000.0,
    lead_screw_pitch_mm: float = 5.0
) -> Dict[str, Any]:
    """
    Calculates rotary quadrature encoder CPR and linear position resolution.
    """
    cpr = ppr * 4  # 4x Quadrature decoding
    
    angular_resolution_deg = 360.0 / cpr if cpr > 0 else 0.09
    angular_resolution_arcsec = angular_resolution_deg * 3600.0
    
    linear_resolution_mm = lead_screw_pitch_mm / cpr if cpr > 0 else 0.001
    linear_resolution_um = linear_resolution_mm * 1000.0
    
    max_pulse_frequency_khz = (cpr * (max_rpm / 60.0)) / 1000.0 if max_rpm > 0 else 100.0

    return {
        "status": "success",
        "pulses_per_revolution_ppr": ppr,
        "quadrature_counts_per_rev_cpr": cpr,
        "max_rpm": max_rpm,
        "angular_resolution_deg": round(angular_resolution_deg, 4),
        "angular_resolution_arcsec": round(angular_resolution_arcsec, 1),
        "linear_position_resolution_um": round(linear_resolution_um, 3),
        "max_pulse_frequency_khz": round(max_pulse_frequency_khz, 1)
    }
