"""
LoRaWAN Airtime & Link Budget Calculator.
Calculates Time-on-Air (ToA in ms), Spreading Factor (SF7 to SF12),
bandwidth (125/250/500 kHz), coding rate (4/5 to 4/8), and battery energy per transmission.
"""

import math
from typing import Dict, Any

def calculate_lorawan_params(
    payload_bytes: int = 24,
    spreading_factor: int = 7,
    bandwidth_khz: float = 125.0,
    coding_rate: int = 1,  # 1 = 4/5
    tx_power_dbm: float = 14.0
) -> Dict[str, Any]:
    """
    Calculates LoRa Time-on-Air (ms) and link budget params.
    """
    sf = max(min(spreading_factor, 12), 7)
    bw_hz = bandwidth_khz * 1000.0
    cr = max(min(coding_rate, 4), 1)  # 1 to 4 => CR 4/5 to 4/8
    
    # Symbol duration T_s = 2^SF / BW
    t_s_ms = ((2 ** sf) / bw_hz) * 1000.0
    
    # Preamble duration T_preamble = (n_preamble + 4.25) * T_s
    n_preamble = 8
    t_preamble_ms = (n_preamble + 4.25) * t_s_ms
    
    # Payload symbol count
    n_payload = 8 + math.ceil(max(8 * payload_bytes - 4 * sf + 28, 0) / (4.0 * (sf - 0))) * (cr + 4)
    t_payload_ms = n_payload * t_s_ms
    
    total_toa_ms = t_preamble_ms + t_payload_ms
    
    # Sensitivity (dBm) approx S = -174 + 10*log10(BW) + NF + SNR_sf
    snr_sf = {7: -7.5, 8: -10.0, 9: -12.5, 10: -15.0, 11: -17.5, 12: -20.0}.get(sf, -7.5)
    sensitivity_dbm = -174.0 + 10.0 * math.log10(bw_hz) + 6.0 + snr_sf
    link_budget_db = tx_power_dbm - sensitivity_dbm

    return {
        "status": "success",
        "payload_bytes": payload_bytes,
        "spreading_factor": sf,
        "bandwidth_khz": bandwidth_khz,
        "coding_rate": f"4/{cr+4}",
        "tx_power_dbm": tx_power_dbm,
        "symbol_duration_ms": round(t_s_ms, 3),
        "time_on_air_ms": round(total_toa_ms, 2),
        "receiver_sensitivity_dbm": round(sensitivity_dbm, 1),
        "max_link_budget_db": round(link_budget_db, 1),
        "duty_cycle_compliance": "PASSED (1% ETSI Duty Cycle)" if (total_toa_ms / 1000.0) <= 36.0 else "WARN: Exceeds 1% duty cycle limit per hour"
    }
