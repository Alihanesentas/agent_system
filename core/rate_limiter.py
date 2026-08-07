"""
LLM API Rate Limiter & Token Bucket Module.
Implements Token Bucket algorithm for API call throttling (e.g. max 60 requests/min)
to eliminate 429 Too Many Requests errors during heavy multi-agent execution.
"""

import time
import threading
from typing import Dict, Any

class TokenBucketRateLimiter:
    def __init__(self, rate_per_sec: float = 2.0, capacity: float = 10.0):
        self.rate = rate_per_sec
        self.capacity = capacity
        self.tokens = capacity
        self.last_fill = time.time()
        self.lock = threading.Lock()

    def acquire(self, tokens_needed: float = 1.0) -> bool:
        with self.lock:
            now = time.time()
            delta = now - self.last_fill
            self.tokens = min(self.capacity, self.tokens + delta * self.rate)
            self.last_fill = now

            if self.tokens >= tokens_needed:
                self.tokens -= tokens_needed
                return True
            return False

    def wait_and_acquire(self, tokens_needed: float = 1.0):
        while not self.acquire(tokens_needed):
            time.sleep(0.1)

global_rate_limiter = TokenBucketRateLimiter(rate_per_sec=2.0, capacity=10.0)
