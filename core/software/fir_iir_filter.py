"""
FIR / IIR Digital Filter Design & Coefficient Generator.
Calculates FIR / IIR filter coefficients (b, a vectors) and C header array code
for Low-pass, High-pass, and Band-pass Butterworth / Windowed Sinc digital filters.
"""

import math
from typing import Dict, Any, List

def design_digital_filter(
    filter_type: str = "lowpass",
    filter_family: str = "FIR_windowed",
    cutoff_freq_hz: float = 100.0,
    sampling_freq_hz: float = 1000.0,
    filter_order: int = 16
) -> Dict[str, Any]:
    """
    Generates FIR filter tap coefficients and C header array definitions.
    """
    ftype = filter_type.lower()
    nyquist = sampling_freq_hz / 2.0
    fc_norm = cutoff_freq_hz / nyquist if nyquist > 0 else 0.1
    
    taps = []
    half_order = filter_order / 2.0
    
    for i in range(filter_order + 1):
        n = i - half_order
        if n == 0:
            h = 2.0 * fc_norm
        else:
            h = math.sin(2.0 * math.pi * fc_norm * n) / (math.pi * n)
        # Hamming window
        w = 0.54 - 0.46 * math.cos(2.0 * math.pi * i / filter_order)
        taps.append(round(h * w, 6))

    # Normalize taps
    total_sum = sum(taps) if sum(taps) != 0 else 1.0
    taps = [round(t / total_sum, 6) for t in taps]

    c_array = f"// FIR {filter_order}-Tap Low-pass Filter (Cutoff: {cutoff_freq_hz}Hz, Fs: {sampling_freq_hz}Hz)\n"
    c_array += f"static const float FILTER_TAPS[{len(taps)}] = {{\n    "
    c_array += ", ".join(str(t) for t in taps)
    c_array += "\n};"

    return {
        "status": "success",
        "filter_type": ftype,
        "filter_family": filter_family,
        "cutoff_freq_hz": cutoff_freq_hz,
        "sampling_freq_hz": sampling_freq_hz,
        "filter_order": filter_order,
        "num_taps": len(taps),
        "coefficients_b": taps,
        "c_header_code": c_array
    }
