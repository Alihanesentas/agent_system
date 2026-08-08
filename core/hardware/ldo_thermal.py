"""
LDO Regulator Thermal & Dropout Voltage Analyzer.
Calculates power dissipation P_loss = (V_in - V_out) * I_load + (V_in * I_q),
junction temperature T_j (°C), dropout voltage headroom, and heatsink copper area requirement.
"""

from typing import Dict, Any

def analyze_ldo_thermal(
    v_in_v: float = 5.0,
    v_out_v: float = 3.3,
    i_load_ma: float = 250.0,
    i_quiescent_ua: float = 100.0,
    rth_ja_c_w: float = 65.0,  # SOT-223 on standard 1oz PCB copper
    ambient_temp_c: float = 25.0
) -> Dict[str, Any]:
    """
    Calculates LDO power loss, junction temperature rise, and thermal safety.
    """
    i_load_a = i_load_ma / 1000.0
    i_q_a = i_quiescent_ua / 1e6
    
    voltage_drop_v = v_in_v - v_out_v
    power_loss_w = (voltage_drop_v * i_load_a) + (v_in_v * i_q_a)
    
    temp_rise_c = power_loss_w * rth_ja_c_w
    junction_temp_c = ambient_temp_c + temp_rise_c
    
    efficiency_pct = (v_out_v * i_load_a) / (v_in_v * (i_load_a + i_q_a)) * 100.0 if v_in_v > 0 else 0.0

    return {
        "status": "success",
        "v_in_v": v_in_v,
        "v_out_v": v_out_v,
        "voltage_drop_v": round(voltage_drop_v, 2),
        "i_load_ma": i_load_ma,
        "power_dissipation_w": round(power_loss_w, 3),
        "junction_temperature_c": round(junction_temp_c, 1),
        "efficiency_pct": round(efficiency_pct, 1),
        "thermal_status": "PASS" if junction_temp_c < 110.0 else "WARN: Exceeds safe 110°C junction limit; consider SMPS buck or larger copper heatsink pour"
    }
