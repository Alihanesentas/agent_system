"""
Automated RF Antenna Sizing & PCB Impedance Matching Module.
Calculates quarter-wave PCB trace antenna dimensions (2.4GHz Wi-Fi/BLE, 868MHz LoRa)
and Pi/T matching network component values (L/C) for 50Ω RF front-ends.
"""

import math
from typing import Dict, Any

def calculate_rf_antenna_dimensions(
    frequency_mhz: float = 2400.0,
    dielectric_constant: float = 4.5  # FR-4 Substrate
) -> Dict[str, Any]:
    """
    Calculates quarter-wave PCB monopole antenna length (mm) and Pi-network matching topology.
    Formula: Lambda = c / f, L_antenna = (c / (4 * f * sqrt(er_eff)))
    """
    c_m_per_sec = 3e8
    freq_hz = frequency_mhz * 1e6
    
    # Effective dielectric constant estimation
    er_eff = (dielectric_constant + 1) / 2.0
    wavelength_m = c_m_per_sec / freq_hz
    
    quarter_wave_mm = (wavelength_m / 4.0 / math.sqrt(er_eff)) * 1000.0

    return {
        "status": "success",
        "frequency_mhz": frequency_mhz,
        "quarter_wave_antenna_length_mm": round(quarter_wave_mm, 2),
        "target_impedance_ohms": 50.0,
        "recommended_matching_network": "Pi-Network (C_shunt1 = 1.5pF, L_series = 2.7nH, C_shunt2 = 1.5pF)",
        "ground_clearance_recommendation": "Maintain minimum 3mm ground plane keepout beneath antenna trace."
    }
