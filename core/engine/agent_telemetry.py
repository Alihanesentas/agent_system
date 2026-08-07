"""
Multi-Agent Execution Gantt & Latency Telemetry Profiler Engine.
Profiles exact step-by-step latency breakdown (ms) across Orchestrator, Planner,
Software, and Hardware sub-agents in real time (/agent-telemetry).
"""

import time
from typing import Dict, Any, List

class AgentTelemetryProfiler:
    def __init__(self):
        self.spans: List[Dict[str, Any]] = []

    def log_agent_span(self, agent_name: str, duration_ms: float):
        """Logs execution latency span for an agent."""
        self.spans.append({
            "agent_name": agent_name,
            "duration_ms": round(duration_ms, 1),
            "timestamp": time.time()
        })

    def get_telemetry_report(self) -> Dict[str, Any]:
        """Returns latency breakdown across sub-agents."""
        total_ms = sum(s["duration_ms"] for s in self.spans)
        return {
            "status": "success",
            "total_execution_ms": round(total_ms, 1),
            "spans_count": len(self.spans),
            "spans_detail": self.spans
        }

global_agent_telemetry = AgentTelemetryProfiler()
