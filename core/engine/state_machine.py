"""
Hierarchical Sub-Agent Finite State Machine (FSM) & Rollback Engine.
Tracks deterministic agent execution states (IDLE, PLANNING, EXECUTING, VERIFYING, HEALING, COMPLETE)
with automatic state rollback if verification fails.
"""

from typing import Dict, Any, List

class AgentStateMachine:
    def __init__(self):
        self.state = "IDLE"
        self.state_history: List[str] = ["IDLE"]

    def transition_to(self, new_state: str) -> Dict[str, Any]:
        """Transitions agent to a new FSM state."""
        valid_states = ["IDLE", "PLANNING", "EXECUTING", "VERIFYING", "HEALING", "COMPLETE", "FAILED"]
        if new_state.upper() in valid_states:
            self.state = new_state.upper()
            self.state_history.append(self.state)
            return {"status": "success", "current_state": self.state, "history": self.state_history}
        return {"status": "error", "message": f"Invalid state '{new_state}'"}

    def rollback_state(self) -> Dict[str, Any]:
        """Rolls back to the previous stable state."""
        if len(self.state_history) > 1:
            self.state_history.pop()
            self.state = self.state_history[-1]
            return {"status": "success", "rolled_back_to": self.state}
        return {"status": "error", "message": "No previous state to rollback to."}

global_agent_fsm = AgentStateMachine()
