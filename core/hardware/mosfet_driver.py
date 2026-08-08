"""
High/Low-Side MOSFET Gate Driver & Switching Loss Sizer.
Calculates gate charge Q_g (nC), peak gate drive current I_pk (A),
switching transition time (ns), conduction loss P_cond (W), and gate driver dissipation.
"""

from typing import Dict, Any

def design_mosfet_driver(
    v_gate_v: float = 10.0,
    gate_charge_nc: float = 45.0,
    r_gate_ohms: float = 10.0,
    r_ds_on_mohm: float = 5.0,
    i_drain_a: float = 20.0,
    switching_freq_khz: float = 100.0
) -> Dict[str, Any]:
    """
    Calculates gate driver peak current, switching power loss, and conduction loss.
    """
    # Peak gate current I_peak = V_gate / R_gate
    i_peak_a = v_gate_v / r_gate_ohms if r_gate_ohms > 0 else 1.0
    
    # Gate drive power loss P_gate = Q_g * V_gate * f_sw
    f_sw_hz = switching_freq_khz * 1000.0
    p_gate_w = (gate_charge_nc * 1e-9) * v_gate_v * f_sw_hz
    
    # Conduction loss P_cond = I_d^2 * R_ds_on
    p_cond_w = (i_drain_a ** 2) * (r_ds_on_mohm / 1000.0)
    
    # Switching transition time t_sw approx Q_g / I_peak
    t_sw_ns = (gate_charge_nc / i_peak_a) if i_peak_a > 0 else 50.0

    return {
        "status": "success",
        "gate_voltage_v": v_gate_v,
        "gate_charge_nc": gate_charge_nc,
        "peak_gate_current_a": round(i_peak_a, 2),
        "switching_time_ns": round(t_sw_ns, 1),
        "gate_drive_power_w": round(p_gate_w, 4),
        "conduction_loss_w": round(p_cond_w, 3),
        "total_mosfet_loss_w": round(p_gate_w + p_cond_w, 3),
        "driver_recommendation": f"Select gate driver rated for minimum {round(i_peak_a * 1.2, 1)}A peak output current."
    }
