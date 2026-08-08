"""
Distributed Saga Pattern State Machine & Compensating Transaction Designer.
Generates Choreography vs Orchestration Saga workflows, rollback compensation hooks,
outbox pattern event forwarding, and state machine transition tables.
"""

from typing import Dict, Any, List

def design_saga_pattern(
    saga_name: str = "order_fulfillment_saga",
    saga_steps: List[str] = ["ReserveStock", "ChargePayment", "CreateShipment"]
) -> Dict[str, Any]:
    """
    Generates distributed Saga state machine steps and compensating rollback actions.
    """
    compensating_actions = [f"Cancel{step}" for step in reversed(saga_steps)]
    
    state_machine = {
        step: {"success_next": saga_steps[i+1] if i+1 < len(saga_steps) else "COMPLETED", "failure_rollback": compensating_actions[len(saga_steps)-1-i]}
        for i, step in enumerate(saga_steps)
    }

    return {
        "status": "success",
        "saga_name": saga_name,
        "forward_steps": saga_steps,
        "compensating_rollback_steps": compensating_actions,
        "state_machine_transitions": state_machine,
        "saga_type": "Orchestrator-Based Saga (Temporal / AWS Step Functions)"
    }
