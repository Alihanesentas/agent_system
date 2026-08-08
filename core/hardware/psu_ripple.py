"""
Power Supply Output Voltage Ripple & Filter Capacitor Calculator.
Calculates peak-to-peak output ripple V_pp (mV), filter capacitance requirement C_out (uF),
and ESR (Equivalent Series Resistance) ripple contribution for SMPS and linear regulators.
"""

from typing import Dict, Any

def analyze_psu_ripple(
    v_out_v: float = 3.3,
    i_load_a: float = 2.0,
    switching_freq_khz: float = 500.0,
    target_ripple_mv: float = 30.0,
    esr_mohm: float = 10.0
) -> Dict[str, Any]:
    """
    Calculates minimum output capacitance and ESR limits for target ripple.
    """
    f_sw_hz = switching_freq_khz * 1000.0
    v_ripple_v = target_ripple_mv / 1000.0
    
    # Capacitive ripple V_c = I_out / (C * f_sw) => C_min = I_out / (V_ripple * f_sw)
    c_min_farads = (i_load_a / (v_ripple_v * f_sw_hz)) if v_ripple_v * f_sw_hz > 0 else 10e-6
    c_min_uf = c_min_farads * 1e6
    
    # ESR ripple voltage V_esr = I_ripple_pp * ESR (assume inductor ripple = 30% of I_out)
    i_ripple_a = i_load_a * 0.3
    v_esr_mv = i_ripple_a * (esr_mohm / 1000.0) * 1000.0
    
    total_ripple_mv = target_ripple_mv + v_esr_mv

    return {
        "status": "success",
        "v_out_v": v_out_v,
        "i_load_a": i_load_a,
        "switching_freq_khz": switching_freq_khz,
        "target_ripple_mv": target_ripple_mv,
        "min_capacitance_uf": round(c_min_uf, 1),
        "esr_ripple_mv": round(v_esr_mv, 2),
        "estimated_total_ripple_mv": round(total_ripple_mv, 2),
        "recommendation": f"Use minimum {round(c_min_uf * 1.5, 0)}uF ceramic MLCC (X7R) with ESR < {esr_mohm}mΩ."
    }
