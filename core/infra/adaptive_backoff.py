"""
API Request Rate Limiter Throttling & Adaptive Backoff Calculator Engine.
Calculates exponential backoff jitter delay (ms) when LLM APIs emit HTTP 429 Rate Limit responses.
"""

import random
from typing import Dict, Any

def calculate_adaptive_backoff_delay(
    retry_attempt: int = 1,
    base_delay_ms: float = 500.0,
    max_delay_ms: float = 10000.0
) -> Dict[str, Any]:
    """Calculates exponential backoff delay with full jitter for API rate limits."""
    exp_delay = base_delay_ms * (2 ** (retry_attempt - 1))
    bounded_delay = min(max_delay_ms, exp_delay)
    jitter_delay_ms = random.uniform(0, bounded_delay)

    return {
        "status": "success",
        "retry_attempt": retry_attempt,
        "bounded_delay_ms": round(bounded_delay, 1),
        "calculated_jitter_delay_ms": round(jitter_delay_ms, 1)
    }
