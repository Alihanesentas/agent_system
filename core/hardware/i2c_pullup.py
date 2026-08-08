"""
I2C Bus Pull-Up Resistor & Rise Time Calculator.
Calculates min/max pull-up resistor values (R_min, R_max) based on I2C bus voltage,
speed mode (100kHz Standard / 400kHz Fast / 1MHz Fast Plus), and total bus capacitance (pF).
"""

from typing import Dict, Any

def calculate_i2c_pullup(
    bus_voltage_v: float = 3.3,
    bus_speed_khz: float = 400.0,
    bus_capacitance_pf: float = 150.0
) -> Dict[str, Any]:
    """
    Calculates min/max and recommended I2C pull-up resistor values.
    """
    # Max rise time (t_r) specs per UM10204 (I2C spec)
    if bus_speed_khz <= 100:
        max_tr_ns = 1000.0
        vol_max_v = 0.4
        iol_min_ma = 3.0
    elif bus_speed_khz <= 400:
        max_tr_ns = 300.0
        vol_max_v = 0.4
        iol_min_ma = 3.0
    else:  # Fast Mode Plus 1MHz
        max_tr_ns = 120.0
        vol_max_v = 0.4
        iol_min_ma = 20.0

    # R_min = (Vcc - V_OL) / I_OL
    r_min_ohms = (bus_voltage_v - vol_max_v) / (iol_min_ma * 1e-3)
    # R_max = t_r / (0.8473 * C_bus)
    r_max_ohms = (max_tr_ns * 1e-9) / (0.8473 * (bus_capacitance_pf * 1e-12))
    
    rec_r_ohms = (r_min_ohms + min(r_max_ohms, 10000.0)) / 2.0
    # Standard E24 rounding
    e24_choices = [1000, 1500, 2200, 3300, 4700, 10000]
    best_resistor = min(e24_choices, key=lambda x: abs(x - rec_r_ohms) if r_min_ohms <= x <= r_max_ohms else 99999)

    return {
        "status": "success",
        "bus_voltage_v": bus_voltage_v,
        "bus_speed_khz": bus_speed_khz,
        "bus_capacitance_pf": bus_capacitance_pf,
        "r_min_ohms": round(r_min_ohms, 1),
        "r_max_ohms": round(r_max_ohms, 1),
        "recommended_r_ohms": best_resistor if best_resistor != 99999 else round(rec_r_ohms, 0),
        "max_rise_time_ns": max_tr_ns,
        "compliance": "PASSED" if r_min_ohms <= best_resistor <= r_max_ohms else "WARN: High bus capacitance",
        "recommendation": f"Use {best_resistor}Ω pull-up resistors on SDA and SCL lines."
    }
