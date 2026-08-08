r"""
RTOS Rate Monotonic (RMS) & Earliest Deadline First (EDF) Scheduler Simulator.
Calculates total CPU utilization U (%), checks Liu & Layland schedulability bound
$U \le n(2^{1/n} - 1)$, and verifies RTOS task deadline feasibility.
"""

import math
from typing import Dict, Any, List

def simulate_scheduler(
    tasks: List[Dict[str, float]] = [
        {"name": "Task_Sensors", "period_ms": 10.0, "execution_ms": 2.0},
        {"name": "Task_Control", "period_ms": 20.0, "execution_ms": 5.0},
        {"name": "Task_Display", "period_ms": 100.0, "execution_ms": 10.0},
    ]
) -> Dict[str, Any]:
    """
    Simulates RMS/EDF task schedulability and CPU utilization.
    """
    n = len(tasks)
    total_u = sum(t["execution_ms"] / t["period_ms"] for t in tasks) if tasks else 0.0
    
    # Liu & Layland bound for RMS = n * (2^(1/n) - 1)
    rms_bound = n * ((2.0 ** (1.0 / n)) - 1.0) if n > 0 else 1.0
    
    rms_schedulable = total_u <= rms_bound
    edf_schedulable = total_u <= 1.0

    return {
        "status": "success",
        "task_count": n,
        "tasks_configured": tasks,
        "total_cpu_utilization_pct": round(total_u * 100.0, 2),
        "rms_utilization_bound_pct": round(rms_bound * 100.0, 2),
        "rms_schedulable": rms_schedulable,
        "edf_schedulable": edf_schedulable,
        "schedulability_verdict": "FEASIBLE" if edf_schedulable else "UNSCHEDULABLE: Overloaded CPU utilization > 100%"
    }
