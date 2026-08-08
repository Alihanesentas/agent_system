"""
LVDS / SerDes High-Speed Differential Signal Integrity Analyzer.
Calculates LVDS differential output swing V_OD (mV), common-mode voltage V_OS (V),
100Ω termination power dissipation (mW), and max data rate (Gbps) jitter budget.
"""

from typing import Dict, Any

def analyze_lvds_signal(
    data_rate_mbps: float = 800.0,
    termination_ohms: float = 100.0,
    driver_current_ma: float = 3.5
) -> Dict[str, Any]:
    """
    Calculates LVDS signal swing, common mode offset, and jitter budget.
    """
    v_od_mv = driver_current_ma * termination_ohms
    v_os_v = 1.2  # Standard LVDS common mode offset
    
    p_term_mw = (driver_current_ma ** 2) * termination_ohms / 1000.0
    
    bit_period_ps = (1000000.0 / data_rate_mbps) if data_rate_mbps > 0 else 1250.0
    max_jitter_ps = bit_period_ps * 0.2  # 20% UI max total jitter

    return {
        "status": "success",
        "data_rate_mbps": data_rate_mbps,
        "termination_resistor_ohms": termination_ohms,
        "differential_swing_vod_mv": round(v_od_mv, 1),
        "offset_voltage_vos_v": v_os_v,
        "termination_power_mw": round(p_term_mw, 2),
        "unit_interval_ui_ps": round(bit_period_ps, 1),
        "max_allowable_jitter_ps": round(max_jitter_ps, 1),
        "compliance": "TIA/EIA-644 LVDS Compliant" if 250.0 <= v_od_mv <= 450.0 else "NON-STANDARD LVDS SWING"
    }
