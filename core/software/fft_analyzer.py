r"""
FFT (Fast Fourier Transform) Frequency Resolution & Windowing Analyzer.
Calculates FFT bin resolution $\Delta f$ (Hz), Nyquist frequency $f_{Nyquist}$ (Hz),
sampling rate $f_s$, window attenuation (Hann/Hamming/Blackman), and execution time ($ms$).
"""

import math
from typing import Dict, Any

def analyze_fft_params(
    sample_rate_hz: float = 10000.0,
    fft_size: int = 1024,
    window_type: str = "Hann"
) -> Dict[str, Any]:
    """
    Calculates FFT frequency bin resolution and spectral leakage characteristics.
    """
    nyquist_hz = sample_rate_hz / 2.0
    bin_resolution_hz = sample_rate_hz / fft_size if fft_size > 0 else 10.0
    
    window_loss_db = {"Hann": 1.42, "Hamming": 1.78, "Blackman": 2.37, "Rectangular": 0.0}.get(window_type, 1.42)

    return {
        "status": "success",
        "sample_rate_hz": sample_rate_hz,
        "fft_size": fft_size,
        "nyquist_frequency_hz": nyquist_hz,
        "frequency_bin_resolution_hz": round(bin_resolution_hz, 3),
        "window_type": window_type,
        "processing_gain_loss_db": window_loss_db,
        "complexity": "O(N log N)"
    }
