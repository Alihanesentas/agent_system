"""
Reverse Polarity Protection Circuit Designer (P-Channel MOSFET vs Schottky).
Compares Schottky diode, P-Channel MOSFET, and Smart Ideal Diode controller topologies,
calculating conduction voltage drop V_drop (mV), power loss P_loss (W), and efficiency.
"""

from typing import Dict, Any

def design_reverse_polarity_protection(
    v_in_v: float = 12.0,
    i_load_a: float = 3.0,
    topology: str = "pmosfet"  # schottky, pmosfet, ideal_diode
) -> Dict[str, Any]:
    """
    Calculates power loss and voltage drop across reverse polarity protection circuits.
    """
    topo = topology.lower().strip()
    
    if "schottky" in topo:
        v_drop_v = 0.45
        p_loss_w = v_drop_v * i_load_a
        description = "Schottky Diode (Simple, cheap, higher power loss)"
    elif "ideal" in topo:
        v_drop_v = 0.02
        p_loss_w = v_drop_v * i_load_a
        description = "Ideal Diode Controller + N-FET (Lowest loss, active controller)"
    else:  # P-FET
        r_ds_on_mohm = 15.0
        v_drop_v = i_load_a * (r_ds_on_mohm / 1000.0)
        p_loss_w = (i_load_a ** 2) * (r_ds_on_mohm / 1000.0)
        description = "P-Channel MOSFET (Low drop, zero quiescent current)"

    efficiency_pct = ((v_in_v - v_drop_v) / v_in_v) * 100.0 if v_in_v > 0 else 0.0

    return {
        "status": "success",
        "topology": topo,
        "description": description,
        "v_in_v": v_in_v,
        "i_load_a": i_load_a,
        "voltage_drop_mv": round(v_drop_v * 1000.0, 1),
        "power_loss_w": round(p_loss_w, 3),
        "efficiency_pct": round(efficiency_pct, 2),
        "v_out_actual_v": round(v_in_v - v_drop_v, 2)
    }
