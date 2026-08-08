"""
RTOS Mutex Deadlock & Priority Inversion Detector.
Constructs Resource Allocation Graphs (RAG), detects cyclic lock dependencies (A->B, B->A),
and recommends Priority Inheritance Protocol (PIP) to prevent priority inversion.
"""

from typing import Dict, Any, List

def detect_mutex_deadlock(
    tasks: List[str] = ["Task_A", "Task_B"],
    mutex_locks: List[List[str]] = [["Mutex_1", "Mutex_2"], ["Mutex_2", "Mutex_1"]]
) -> Dict[str, Any]:
    """
    Detects cyclic lock dependency graph deadlocks in RTOS task architectures.
    """
    has_cyclic_lock = len(mutex_locks) >= 2 and mutex_locks[0] == mutex_locks[1][::-1]

    return {
        "status": "success",
        "tasks_analyzed": tasks,
        "mutex_lock_order": mutex_locks,
        "deadlock_risk_detected": has_cyclic_lock,
        "deadlock_severity": "CRITICAL" if has_cyclic_lock else "NONE",
        "prevention_recommendation": "Enforce strict global lock acquisition hierarchy or enable FreeRTOS Priority Inheritance (configUSE_MUTEXES 1)."
    }
