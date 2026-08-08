r"""
Fluid Pipe Flow Reynolds Number & Pressure Drop ($\Delta P$) Calculator.
Calculates Reynolds number $Re$, flow regime (Laminar / Turbulent), Darcy friction factor $f$,
head loss $h_f$ ($m$), and pressure drop $\Delta P$ ($kPa$) via Darcy-Weisbach equation.
"""

import math
from typing import Dict, Any

def calculate_pipe_flow(
    flow_rate_lpm: float = 20.0,
    pipe_inner_diameter_mm: float = 15.0,
    pipe_length_m: float = 5.0,
    fluid_density_kg_m3: float = 1000.0,  # Water
    dynamic_viscosity_pa_s: float = 0.001  # Water 1 cP
) -> Dict[str, Any]:
    """
    Calculates pipe flow velocity, Reynolds number, and friction pressure drop.
    """
    d_m = pipe_inner_diameter_mm / 1000.0
    q_m3_s = (flow_rate_lpm / 60000.0)
    
    area_m2 = math.pi * ((d_m / 2.0) ** 2)
    velocity_m_s = q_m3_s / area_m2 if area_m2 > 0 else 0.0
    
    # Reynolds Number Re = (density * velocity * D) / viscosity
    reynolds = (fluid_density_kg_m3 * velocity_m_s * d_m) / dynamic_viscosity_pa_s if dynamic_viscosity_pa_s > 0 else 2000.0
    
    if reynolds < 2300:
        regime = "Laminar Flow"
        f = 64.0 / reynolds if reynolds > 0 else 0.03
    else:
        regime = "Turbulent Flow"
        f = 0.3164 / (reynolds ** 0.25)  # Blasius formula
        
    # Pressure drop deltaP = f * (L / D) * (density * v^2 / 2)
    delta_p_pa = f * (pipe_length_m / d_m) * (fluid_density_kg_m3 * (velocity_m_s ** 2) / 2.0) if d_m > 0 else 0.0
    delta_p_kpa = delta_p_pa / 1000.0

    return {
        "status": "success",
        "flow_rate_lpm": flow_rate_lpm,
        "pipe_inner_diameter_mm": pipe_inner_diameter_mm,
        "flow_velocity_m_s": round(velocity_m_s, 2),
        "reynolds_number": round(reynolds, 0),
        "flow_regime": regime,
        "darcy_friction_factor": round(f, 4),
        "pressure_drop_kpa": round(delta_p_kpa, 2)
    }
