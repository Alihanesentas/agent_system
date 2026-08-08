"""
Interrupt Service Routine (ISR) Latency & Nested Interrupt Analyzer.
Calculates NVIC interrupt latency (cycles / μs), context save/restore overhead,
jitter, and worst-case execution time (WCET) for Cortex-M / RISC-V ISRs.
"""

from typing import Dict, Any

def analyze_isr_latency(
    mcu_clock_mhz: float = 160.0,
    nvic_hardware_latency_cycles: int = 12,  # Cortex-M4 stack push cycles
    isr_instruction_count: int = 45,
    nested_interrupts_allowed: bool = True
) -> Dict[str, Any]:
    """
    Calculates ISR entry latency, execution time, and exit overhead.
    """
    cycle_time_us = 1.0 / mcu_clock_mhz if mcu_clock_mhz > 0 else 0.00625
    
    entry_latency_us = nvic_hardware_latency_cycles * cycle_time_us
    exec_time_us = isr_instruction_count * cycle_time_us
    exit_overhead_us = 10 * cycle_time_us  # Unstacking cycles
    
    wcet_us = entry_latency_us + exec_time_us + exit_overhead_us
    if nested_interrupts_allowed:
        wcet_us *= 1.35  # 35% jitter margin for preemption

    return {
        "status": "success",
        "mcu_clock_mhz": mcu_clock_mhz,
        "entry_hardware_latency_cycles": nvic_hardware_latency_cycles,
        "entry_latency_us": round(entry_latency_us, 3),
        "isr_execution_time_us": round(exec_time_us, 3),
        "exit_overhead_us": round(exit_overhead_us, 3),
        "worst_case_execution_time_us": round(wcet_us, 3),
        "max_recommended_trigger_rate_khz": round(1000.0 / (wcet_us * 2.0), 1) if wcet_us > 0 else 500.0,
        "latency_rating": "OPTIMAL (Sub-microsecond)" if wcet_us < 1.0 else "PASSABLE"
    }
