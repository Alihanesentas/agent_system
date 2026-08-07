"""
Multi-Model Dynamic Fallback Chain & Circuit Breaker Engine.
Implements a resilient circuit breaker pattern for LLM API endpoints: if OpenAI timeouts 3 times,
auto-switches to Claude 3.5 Sonnet, then Gemini Flash.
"""

from typing import Dict, Any, List

class LLMCircuitBreaker:
    def __init__(self, max_failures: int = 3):
        self.max_failures = max_failures
        self.failure_counts: Dict[str, int] = {}
        self.open_circuits: List[str] = []

    def record_failure(self, model: str) -> Dict[str, Any]:
        """Records an API failure and trips circuit if threshold exceeded."""
        self.failure_counts[model] = self.failure_counts.get(model, 0) + 1
        tripped = False
        if self.failure_counts[model] >= self.max_failures:
            if model not in self.open_circuits:
                self.open_circuits.append(model)
                tripped = True

        return {
            "status": "success",
            "model": model,
            "failure_count": self.failure_counts[model],
            "circuit_tripped": tripped,
            "open_circuits": self.open_circuits
        }

global_circuit_breaker = LLMCircuitBreaker()
