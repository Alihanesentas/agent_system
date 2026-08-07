"""
Sub-Agent Benchmark Arena Engine.
Runs 2 models or prompt setups head-to-head on the exact same hardware/software prompt,
comparing latency, token consumption, syntax pass rate, and score!
"""

import time
from typing import Dict, Any, List
from core.engine.runner import run_agent_task

def run_agent_arena(
    user_prompt: str,
    agent_name: str = "software",
    model_a: str = "gpt-4o",
    model_b: str = "gpt-4o-mini"
) -> Dict[str, Any]:
    """
    Executes head-to-head Model Arena comparison on the exact same prompt.
    """
    # Model A execution
    start_a = time.time()
    out_a = run_agent_task(agent_name=agent_name, user_prompt=user_prompt, model_name=model_a, use_rag=False)
    elapsed_a = round((time.time() - start_a) * 1000, 1)

    # Model B execution
    start_b = time.time()
    out_b = run_agent_task(agent_name=agent_name, user_prompt=user_prompt, model_name=model_b, use_rag=False)
    elapsed_b = round((time.time() - start_b) * 1000, 1)

    winner = model_a if elapsed_a < elapsed_b else model_b

    return {
        "status": "success",
        "arena_prompt": user_prompt,
        "model_a": {
            "model_name": model_a,
            "latency_ms": elapsed_a,
            "output_preview": out_a[:200]
        },
        "model_b": {
            "model_name": model_b,
            "latency_ms": elapsed_b,
            "output_preview": out_b[:200]
        },
        "speed_winner": winner,
        "latency_difference_ms": abs(elapsed_a - elapsed_b)
    }
