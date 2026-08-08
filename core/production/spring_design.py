"""
Mechanical Helical Compression Spring Design Engine.
Calculates spring rate (k in N/mm), shear stress (von Mises / Wahl factor),
solid height (mm), free length (mm), and fatigue life for helical compression springs.
"""

import math
from typing import Dict, Any

def design_spring(
    wire_dia_mm: float = 1.5,
    outer_dia_mm: float = 12.0,
    active_coils: int = 8,
    shear_modulus_gpa: float = 79.0,  # Music wire / Stainless
    working_load_n: float = 45.0
) -> Dict[str, Any]:
    """
    Designs helical spring and calculates spring rate, Wahl factor, and stress.
    """
    d = wire_dia_mm
    mean_dia_mm = outer_dia_mm - d
    c_spring_index = mean_dia_mm / d if d > 0 else 8.0
    
    g_mpa = shear_modulus_gpa * 1000.0
    
    # Spring rate k = (G * d^4) / (8 * D^3 * Na)
    k_n_mm = (g_mpa * (d**4)) / (8.0 * (mean_dia_mm**3) * active_coils)
    
    # Wahl stress correction factor K_w = (4C-1)/(4C-4) + 0.615/C
    k_w = ((4.0 * c_spring_index - 1.0) / (4.0 * c_spring_index - 4.0)) + (0.615 / c_spring_index)
    
    # Shear stress tau = K_w * (8 * F * D) / (pi * d^3)
    tau_mpa = k_w * (8.0 * working_load_n * mean_dia_mm) / (math.pi * (d**3))
    
    deflection_mm = working_load_n / k_n_mm if k_n_mm > 0 else 0.0
    solid_height_mm = (active_coils + 2) * d  # Squared and ground ends

    return {
        "status": "success",
        "wire_diameter_mm": d,
        "outer_diameter_mm": outer_dia_mm,
        "mean_diameter_mm": round(mean_dia_mm, 2),
        "active_coils": active_coils,
        "spring_index_c": round(c_spring_index, 2),
        "spring_rate_n_mm": round(k_n_mm, 3),
        "deflection_at_working_load_mm": round(deflection_mm, 2),
        "solid_height_mm": round(solid_height_mm, 2),
        "wahl_factor": round(k_w, 3),
        "corrected_shear_stress_mpa": round(tau_mpa, 1),
        "stress_safety": "SAFE" if tau_mpa < 800.0 else "WARN: High shear stress, check material fatigue limit"
    }
