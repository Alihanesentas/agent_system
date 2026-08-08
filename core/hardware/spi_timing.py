"""
SPI Bus Timing, Clock Phase/Polarity & Setup/Hold Time Analyzer.
Calculates SPI SCK clock period (ns), data setup time t_SU (ns), data hold time t_H (ns),
propagation delay overhead, and SPI mode (Mode 0, 1, 2, 3) compatibility.
"""

from typing import Dict, Any

def analyze_spi_timing(
    clock_freq_mhz: float = 20.0,
    setup_time_req_ns: float = 10.0,
    hold_time_req_ns: float = 10.0,
    cpol: int = 0,  # 0 or 1
    cpha: int = 0   # 0 or 1
) -> Dict[str, Any]:
    """
    Analyzes SPI SCK clock timing margins and Mode configuration.
    """
    sck_period_ns = (1000.0 / clock_freq_mhz) if clock_freq_mhz > 0 else 50.0
    half_period_ns = sck_period_ns / 2.0
    
    setup_margin_ns = half_period_ns - setup_time_req_ns
    hold_margin_ns = half_period_ns - hold_time_req_ns
    
    # SPI Mode calculation: Mode = CPOL * 2 + CPHA
    spi_mode = (cpol * 2) + cpha

    return {
        "status": "success",
        "clock_freq_mhz": clock_freq_mhz,
        "sck_period_ns": round(sck_period_ns, 2),
        "half_period_ns": round(half_period_ns, 2),
        "spi_mode": spi_mode,
        "cpol": cpol,
        "cpha": cpha,
        "setup_time_margin_ns": round(setup_margin_ns, 2),
        "hold_time_margin_ns": round(hold_margin_ns, 2),
        "timing_status": "PASSED" if setup_margin_ns >= 0 and hold_margin_ns >= 0 else "WARN: Inadequate setup/hold time margin at target SPI clock rate"
    }
