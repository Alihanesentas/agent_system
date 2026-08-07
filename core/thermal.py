"""
Automated Thermal & Power Dissipation Analyzer.
Calculates junction temperature (Tj), power dissipation (Pd), thermal resistance (Theta_JA),
and heatsink sizing requirements for LDOs, MOSFETs, and power ICs.
"""

from typing import Dict, Any

def analyze_thermal_dissipation(
    input_voltage: float,
    output_voltage: float,
    current_amps: float,
    theta_ja_cw: float = 65.0,  # °C/W for SOT-223
    max_ambient_temp_c: float = 50.0,
    max_junction_temp_c: float = 125.0
) -> Dict[str, Any]:
    """
    Calculates linear regulator or MOSFET power dissipation and junction temperature.
    Formula: Pd = (Vin - Vout) * Iout
             Tj = Ta + (Pd * Theta_JA)
    """
    v_drop = input_voltage - output_voltage
    power_watts = v_drop * current_amps

    temp_rise_c = power_watts * theta_ja_cw
    junction_temp_c = max_ambient_temp_c + temp_rise_c

    heatsink_required = junction_temp_c > max_junction_temp_c
    recommended_heatsink_theta_sa = 0.0

    if heatsink_required:
        # Theta_SA = ((Tj_max - Ta_max) / Pd) - Theta_JC - Theta_CS
        theta_total_needed = (max_junction_temp_c - max_ambient_temp_c) / power_watts
        recommended_heatsink_theta_sa = max(0.5, round(theta_total_needed - 15.0, 1))

    return {
        "status": "success",
        "power_dissipation_watts": round(power_watts, 2),
        "temperature_rise_c": round(temp_rise_c, 1),
        "calculated_junction_temp_c": round(junction_temp_c, 1),
        "max_junction_temp_limit_c": max_junction_temp_c,
        "thermal_status": "CRITICAL OVERHEATING 🔴" if heatsink_required else "Safe Thermal Range ✅",
        "heatsink_required": heatsink_required,
        "recommended_heatsink_rating_cw": recommended_heatsink_theta_sa if heatsink_required else "None"
    }
