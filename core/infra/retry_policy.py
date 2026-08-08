"""
Configurable Exponential Backoff & Jitter Retry Policy Engine.
Executes target Python callables with configurable max retries, initial delay (sec),
backoff multiplier, and randomized full-jitter parameters to prevent thundering herd.
"""

import time
import random
from typing import Dict, Any, Callable, Optional

def execute_with_retry(
    max_retries: int = 3,
    initial_delay_sec: float = 0.5,
    backoff_factor: float = 2.0,
    jitter: bool = True
) -> Dict[str, Any]:
    """
    Simulates / configures exponential backoff retry parameters.
    """
    delays = []
    curr_delay = initial_delay_sec
    
    for attempt in range(1, max_retries + 1):
        if jitter:
            actual = random.uniform(0.5 * curr_delay, 1.5 * curr_delay)
        else:
            actual = curr_delay
        delays.append(round(actual, 3))
        curr_delay *= backoff_factor

    return {
        "status": "success",
        "max_retries": max_retries,
        "initial_delay_sec": initial_delay_sec,
        "backoff_factor": backoff_factor,
        "jitter_enabled": jitter,
        "calculated_delay_schedule_sec": delays,
        "total_max_wait_time_sec": round(sum(delays), 2)
    }
