"""
ADC Performance & SNR / ENOB Analyzer.
Calculates Signal-to-Noise Ratio (SNR), Effective Number of Bits (ENOB),
quantization noise (uV), dynamic range (dB), and sampling bandwidth for N-bit ADCs.
"""

import math
from typing import Dict, Any

def analyze_adc_performance(
    resolution_bits: int = 12,
    v_ref_v: float = 3.3,
    sampling_rate_ksps: float = 100.0,
    measured_sinad_db: float = 68.0
) -> Dict[str, Any]:
    """
    Calculates theoretical vs measured ADC performance metrics.
    """
    # Theoretical ideal SNR = 6.02 * N + 1.76 dB
    ideal_snr_db = (6.02 * resolution_bits) + 1.76
    
    # ENOB = (SINAD - 1.76) / 6.02
    enob = (measured_sinad_db - 1.76) / 6.02
    
    # LSB size in uV
    lsb_size_uv = (v_ref_v / (2 ** resolution_bits)) * 1e6
    quantization_noise_uv = lsb_size_uv / math.sqrt(12.0)
    nyquist_bandwidth_khz = sampling_rate_ksps / 2.0

    return {
        "status": "success",
        "resolution_bits": resolution_bits,
        "v_ref_v": v_ref_v,
        "sampling_rate_ksps": sampling_rate_ksps,
        "theoretical_snr_db": round(ideal_snr_db, 2),
        "measured_sinad_db": measured_sinad_db,
        "effective_number_of_bits_enob": round(enob, 2),
        "lsb_size_uv": round(lsb_size_uv, 2),
        "quantization_noise_uv": round(quantization_noise_uv, 2),
        "nyquist_bandwidth_khz": round(nyquist_bandwidth_khz, 1),
        "performance_rating": "EXCELLENT" if enob >= resolution_bits - 1.5 else "WARN: Noise / Jitter degradation"
    }
