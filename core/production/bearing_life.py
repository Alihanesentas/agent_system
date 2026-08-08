"""
ISO 281 Ball & Roller Bearing L10 Life Calculator.
Calculates basic rating life L10 (million revolutions), L10h operating hours,
equivalent dynamic load P (N), and dynamic load rating C (N) for ball vs roller bearings.
"""

from typing import Dict, Any

def calculate_bearing_life(
    dynamic_capacity_c_n: float = 14000.0,  # 6204 ball bearing C rating
    radial_load_fr_n: float = 1200.0,
    axial_load_fa_n: float = 300.0,
    operating_rpm: float = 1500.0,
    bearing_type: str = "ball"  # ball (p=3), roller (p=10/3)
) -> Dict[str, Any]:
    """
    Calculates ISO 281 L10 bearing lifespan in million revolutions and operating hours.
    """
    # Equivalent dynamic load P = X*Fr + Y*Fa approx
    p_load_n = radial_load_fr_n + 0.5 * axial_load_fa_n
    
    p_exp = 3.0 if "ball" in bearing_type.lower() else (10.0 / 3.0)
    
    # L10 = (C / P)^p  (in million revolutions)
    l10_mrev = (dynamic_capacity_c_n / p_load_n) ** p_exp if p_load_n > 0 else 1000.0
    
    # L10h = (10^6 * L10) / (60 * RPM)
    l10h_hours = (1e6 * l10_mrev) / (60.0 * operating_rpm) if operating_rpm > 0 else 100000.0

    return {
        "status": "success",
        "bearing_type": bearing_type,
        "dynamic_capacity_c_n": dynamic_capacity_c_n,
        "equivalent_load_p_n": round(p_load_n, 1),
        "operating_rpm": operating_rpm,
        "l10_million_revolutions": round(l10_mrev, 2),
        "l10h_operating_hours": round(l10h_hours, 1),
        "service_years_continuous": round(l10h_hours / (24.0 * 365.25), 2),
        "life_assessment": "SUFFICIENT (L10h > 20,000h)" if l10h_hours >= 20000.0 else "WARN: High load / speed reduces bearing service life below 20,000h"
    }
