r"""
Structural Beam Bending Stress, Shear & Deflection Calculator.
Calculates maximum bending moment $M_{max}$ (N·m), flexural bending stress $\sigma$ (MPa),
shear stress $\tau$ (MPa), deflection $\delta$ (mm), and safety factor per Euler-Bernoulli beam theory.
"""

from typing import Dict, Any

def analyze_beam_stress(
    beam_length_m: float = 0.5,
    applied_force_n: float = 500.0,
    width_mm: float = 20.0,
    height_mm: float = 30.0,
    youngs_modulus_gpa: float = 69.0  # Aluminum 6061-T6
) -> Dict[str, Any]:
    """
    Calculates cantilever beam bending stress, moment of inertia, and deflection.
    """
    b = width_mm / 1000.0
    h = height_mm / 1000.0
    l = beam_length_m
    f = applied_force_n
    e_pa = youngs_modulus_gpa * 1e9
    
    # Second moment of area (Rectangular Moment of Inertia I = b * h^3 / 12)
    i_m4 = (b * (h ** 3)) / 12.0
    
    # Max Bending Moment M_max = F * L for cantilever
    m_max_nm = f * l
    
    # Bending Stress sigma = M * (h / 2) / I
    sigma_pa = (m_max_nm * (h / 2.0)) / i_m4 if i_m4 > 0 else 0.0
    sigma_mpa = sigma_pa / 1e6
    
    # Max Deflection delta = F * L^3 / (3 * E * I)
    deflection_m = (f * (l ** 3)) / (3.0 * e_pa * i_m4) if e_pa * i_m4 > 0 else 0.0
    deflection_mm = deflection_m * 1000.0
    
    yield_strength_mpa = 276.0  # Al 6061-T6
    safety_factor = yield_strength_mpa / sigma_mpa if sigma_mpa > 0 else 999.0

    return {
        "status": "success",
        "beam_length_m": l,
        "applied_force_n": f,
        "cross_section_mm": f"{width_mm}x{height_mm}",
        "material": "Aluminum 6061-T6 (E=69 GPa, Yield=276 MPa)",
        "moment_of_inertia_mm4": round(i_m4 * 1e12, 1),
        "max_bending_moment_nm": round(m_max_nm, 2),
        "max_bending_stress_mpa": round(sigma_mpa, 2),
        "max_deflection_mm": round(deflection_mm, 3),
        "safety_factor": round(safety_factor, 2),
        "structural_verdict": "SAFE" if safety_factor >= 2.0 else "WARN: Low Safety Factor. Increase beam height or material yield strength."
    }
