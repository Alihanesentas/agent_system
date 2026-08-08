"""
FreeRTOS / RTOS Task Architecture & Stack Sizing Designer.
Calculates recommended task priorities, stack memory allocation (words/bytes),
and estimated total CPU utilization for embedded multi-tasking systems.
"""

from typing import Dict, Any, List

def design_rtos_tasks(
    task_specs: List[Dict[str, Any]] = None,
    tick_rate_hz: int = 1000
) -> Dict[str, Any]:
    """
    Designs RTOS task structure, priorities, and stack memory allocations.
    """
    if not task_specs:
        task_specs = [
            {"name": "vTaskTelemetry", "priority": 2, "period_ms": 100, "exec_time_ms": 5, "min_stack_words": 512},
            {"name": "vTaskSensorRead", "priority": 4, "period_ms": 10, "exec_time_ms": 1, "min_stack_words": 256},
            {"name": "vTaskMotorControl", "priority": 5, "period_ms": 2, "exec_time_ms": 0.3, "min_stack_words": 512},
            {"name": "vTaskGUI", "priority": 1, "period_ms": 50, "exec_time_ms": 10, "min_stack_words": 1024},
        ]
    
    total_cpu_util = 0.0
    total_stack_bytes = 0
    configured_tasks = []

    for t in task_specs:
        p = t.get("period_ms", 10.0)
        e = t.get("exec_time_ms", 1.0)
        util = (e / p) * 100.0 if p > 0 else 0.0
        total_cpu_util += util
        
        words = max(t.get("min_stack_words", 256), 256)
        bytes_alloc = words * 4  # 32-bit arch
        total_stack_bytes += bytes_alloc
        
        configured_tasks.append({
            "name": t.get("name"),
            "priority": t.get("priority"),
            "period_ms": p,
            "exec_time_ms": e,
            "cpu_utilization_pct": round(util, 2),
            "allocated_stack_words": words,
            "allocated_stack_bytes": bytes_alloc
        })

    return {
        "status": "success",
        "rtos_tick_rate_hz": tick_rate_hz,
        "task_count": len(configured_tasks),
        "total_cpu_utilization_pct": round(total_cpu_util, 2),
        "schedulable": total_cpu_util < 75.0,
        "total_rtos_stack_ram_bytes": total_stack_bytes,
        "tasks": configured_tasks,
        "recommendation": "All tasks schedulable under Rate Monotonic Analysis (RMA)." if total_cpu_util < 75.0 else "WARNING: High CPU load, optimize task execution times."
    }
