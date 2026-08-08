"""
Operational Amplifier Circuit Design & Bandwidth Engine.
Calculates closed-loop gain (dB / V/V), bandwidth (GBP / Gain), feedback resistor values,
and input impedance for Inverting, Non-Inverting, and Differential Op-Amp configurations.
"""

from typing import Dict, Any

def calculate_opamp_circuit(
    topology: str = "non-inverting",
    target_gain_v_v: float = 10.0,
    r_in_kohm: float = 10.0,
    opamp_gbp_mhz: float = 10.0
) -> Dict[str, Any]:
    """
    Calculates feedback resistors, closed-loop gain, and bandwidth for Op-Amp circuits.
    """
    topo = topology.lower().strip()
    
    if "invert" in topo and "non" not in topo:
        # Inverting: Gain = -Rf / Rin => Rf = Gain * Rin
        rf_kohm = target_gain_v_v * r_in_kohm
        actual_gain = - (rf_kohm / r_in_kohm)
        zin_kohm = r_in_kohm
    elif "diff" in topo:
        # Differential: Gain = R2 / R1
        rf_kohm = target_gain_v_v * r_in_kohm
        actual_gain = rf_kohm / r_in_kohm
        zin_kohm = 2.0 * r_in_kohm
    else:  # Non-inverting: Gain = 1 + (Rf / R1) => Rf = (Gain - 1) * R1
        rf_kohm = (target_gain_v_v - 1.0) * r_in_kohm if target_gain_v_v > 1.0 else 0.0
        actual_gain = 1.0 + (rf_kohm / r_in_kohm)
        zin_kohm = 10000.0  # High impedance (~10M)

    # Bandwidth = GBP / Gain
    bandwidth_khz = (opamp_gbp_mhz * 1000.0) / abs(actual_gain) if abs(actual_gain) > 0 else 0.0

    return {
        "status": "success",
        "topology": topo,
        "opamp_gbp_mhz": opamp_gbp_mhz,
        "target_gain_v_v": target_gain_v_v,
        "calculated_gain_v_v": round(actual_gain, 2),
        "calculated_gain_db": round(20.0 * (math_log10(abs(actual_gain)) if abs(actual_gain) > 0 else 0), 2),
        "recommended_r_in_kohm": r_in_kohm,
        "recommended_r_feedback_kohm": round(rf_kohm, 2),
        "input_impedance_kohm": round(zin_kohm, 1),
        "bandwidth_3db_khz": round(bandwidth_khz, 1)
    }

def math_log10(x: float) -> float:
    import math
    return math.log10(x)
