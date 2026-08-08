"""
CAN Bus Bit Timing & Termination Calculator.
Calculates nominal bit rate, bit segment parameters (Prop_Seg, Phase_Seg1, Phase_Seg2, SJW),
prescaler values, and 120Ω termination network specs for CAN 2.0B and CAN-FD.
"""

from typing import Dict, Any

def configure_can_bus(
    target_baud_kbps: int = 500,
    mcu_clock_mhz: float = 80.0,
    sample_point_pct: float = 87.5
) -> Dict[str, Any]:
    """
    Calculates CAN bus bit timing segments and prescaler settings.
    """
    baud_hz = target_baud_kbps * 1000.0
    clock_hz = mcu_clock_mhz * 1e6
    
    # Target time quanta TQ count per bit (standard 16 TQ)
    tq_per_bit = 16
    prescaler = int(clock_hz / (baud_hz * tq_per_bit))
    
    actual_baud = clock_hz / (prescaler * tq_per_bit)
    
    # Segment allocations: Sync_Seg = 1 TQ
    sample_tq = int(tq_per_bit * (sample_point_pct / 100.0))
    prop_seg = max(sample_tq - 4, 1)
    phase_seg1 = max(sample_tq - 1 - prop_seg, 1)
    phase_seg2 = tq_per_bit - (1 + prop_seg + phase_seg1)
    sjw = min(phase_seg2, 4)

    return {
        "status": "success",
        "target_baud_kbps": target_baud_kbps,
        "actual_baud_kbps": round(actual_baud / 1000.0, 2),
        "mcu_clock_mhz": mcu_clock_mhz,
        "prescaler": prescaler,
        "time_quanta_per_bit": tq_per_bit,
        "segments": {
            "sync_seg": 1,
            "prop_seg": prop_seg,
            "phase_seg1": phase_seg1,
            "phase_seg2": phase_seg2,
            "sjw": sjw
        },
        "calculated_sample_point_pct": round(((1 + prop_seg + phase_seg1) / tq_per_bit) * 100.0, 1),
        "termination_recommendation": "Place 120Ω 1% 0.25W resistor across CANH and CANL at both end nodes of the bus."
    }
