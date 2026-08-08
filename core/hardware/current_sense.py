"""
Shunt Resistor & INA Current Sense Circuit Designer.
Calculates shunt resistor R_sense (mΩ), power dissipation P_shunt (W),
amplifier gain requirement, and output voltage V_out for INA219 / INA180 current monitors.
"""

from typing import Dict, Any

def design_current_sense(
    max_current_a: float = 10.0,
    max_shunt_voltage_mv: float = 50.0,
    amplifier_gain: float = 20.0
) -> Dict[str, Any]:
    """
    Calculates current sense shunt value, power dissipation, and amplifier output.
    """
    # R_sense = V_sense_max / I_max
    r_sense_mohm = (max_shunt_voltage_mv / max_current_a) if max_current_a > 0 else 10.0
    
    # Power loss P = I^2 * R
    p_loss_w = (max_current_a ** 2) * (r_sense_mohm / 1000.0)
    
    v_out_max_v = (max_shunt_voltage_mv / 1000.0) * amplifier_gain

    return {
        "status": "success",
        "max_current_a": max_current_a,
        "max_shunt_voltage_mv": max_shunt_voltage_mv,
        "recommended_r_sense_mohm": round(r_sense_mohm, 2),
        "shunt_power_dissipation_w": round(p_loss_w, 3),
        "recommended_resistor_wattage": f"{round(p_loss_w * 2.0, 2)}W (2x safety margin)",
        "amplifier_gain": amplifier_gain,
        "max_output_voltage_v": round(v_out_max_v, 2)
    }
