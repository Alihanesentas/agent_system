"""
Precision Resistor Voltage Divider Calculator.
Computes R1/R2 standard E96/E24 resistor pairs for feedback networks, ADC reference scaling,
and battery voltage sense dividers.
"""

from typing import Dict, Any

E24_SERIES = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]

def calculate_voltage_divider(
    vin_v: float = 12.0,
    target_vout_v: float = 3.3,
    max_quiescent_ua: float = 500.0
) -> Dict[str, Any]:
    """
    Calculates precision resistor voltage divider values.
    """
    target_ratio = target_vout_v / vin_v if vin_v > 0 else 0.5
    req_total_r = (vin_v / (max_quiescent_ua * 1e-6)) if max_quiescent_ua > 0 else 100000.0
    
    r2_target = req_total_r * target_ratio
    r1_target = req_total_r - r2_target

    # Scale to standard E24 values
    def find_nearest_e24(val):
        exponent = 10 ** (len(str(int(val))) - 1) if val >= 10 else 1.0
        scaled = val / exponent if exponent > 0 else val
        closest = min(E24_SERIES, key=lambda x: abs(x - scaled))
        return closest * exponent

    r1_e24 = find_nearest_e24(r1_target)
    r2_e24 = find_nearest_e24(r2_target)

    actual_vout = vin_v * (r2_e24 / (r1_e24 + r2_e24))
    quiescent_ua = (vin_v / (r1_e24 + r2_e24)) * 1e6
    power_loss_mw = (vin_v ** 2 / (r1_e24 + r2_e24)) * 1000.0
    error_pct = abs((actual_vout - target_vout_v) / target_vout_v) * 100.0

    return {
        "status": "success",
        "vin_v": vin_v,
        "target_vout_v": target_vout_v,
        "recommended_r1_ohms": int(r1_e24),
        "recommended_r2_ohms": int(r2_e24),
        "actual_vout_v": round(actual_vout, 3),
        "error_pct": round(error_pct, 2),
        "quiescent_current_ua": round(quiescent_ua, 2),
        "power_dissipation_mw": round(power_loss_mw, 3),
        "e24_series": True
    }
