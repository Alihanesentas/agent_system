"""
SMPS (Switch-Mode Power Supply) Buck/Boost Converter Design Engine.
Calculates inductor value (uH), output capacitor (uF), MOSFET peak current (A),
and estimated efficiency (%) for DC-DC Buck and Boost converters.
"""

import math
from typing import Dict, Any

def design_smps_converter(
    topology: str = "buck",
    vin_v: float = 12.0,
    vout_v: float = 5.0,
    iout_a: float = 2.0,
    fsw_khz: float = 300.0,
    vripple_mv: float = 50.0
) -> Dict[str, Any]:
    """
    Designs SMPS Buck or Boost converter components.
    """
    fsw_hz = fsw_khz * 1000.0
    vripple_v = vripple_mv / 1000.0
    
    if topology.lower() == "buck":
        duty_cycle = vout_v / vin_v if vin_v > 0 else 0.416
        # Target inductor ripple current ~30% of Iout
        delta_il = 0.3 * iout_a
        l_min_uh = ((vin_v - vout_v) * duty_cycle) / (delta_il * fsw_hz) * 1e6
        cout_min_uf = (delta_il / (8 * fsw_hz * vripple_v)) * 1e6
        ipeak_a = iout_a + (delta_il / 2.0)
        est_eff = 91.5 - (0.5 * (vin_v - vout_v))
    else:  # boost
        duty_cycle = 1.0 - (vin_v / vout_v) if vout_v > 0 else 0.583
        delta_il = 0.3 * (iout_a * (vout_v / vin_v))
        l_min_uh = (vin_v * duty_cycle) / (delta_il * fsw_hz) * 1e6
        cout_min_uf = (iout_a * duty_cycle) / (fsw_hz * vripple_v) * 1e6
        ipeak_a = (iout_a / (1.0 - duty_cycle)) + (delta_il / 2.0)
        est_eff = 88.0 - (0.3 * (vout_v - vin_v))

    return {
        "status": "success",
        "topology": topology.lower(),
        "input_voltage_v": vin_v,
        "output_voltage_v": vout_v,
        "output_current_a": iout_a,
        "switching_frequency_khz": fsw_khz,
        "duty_cycle": round(duty_cycle, 4),
        "recommended_inductor_uh": round(max(l_min_uh * 1.2, 1.0), 2),
        "recommended_capacitor_uf": round(max(cout_min_uf * 1.5, 10.0), 1),
        "peak_mosfet_current_a": round(ipeak_a, 2),
        "estimated_efficiency_pct": round(min(max(est_eff, 75.0), 96.0), 1),
        "recommendation": f"Use {round(max(l_min_uh * 1.2, 1.0), 1)}uH inductor rated for >{round(ipeak_a * 1.3, 1)}A saturation current."
    }
