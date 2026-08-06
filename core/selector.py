import sqlite3
import os
from typing import Dict, Any, List, Optional
from subagent_tracker.backend.tracker import count_tokens, calculate_cost, MODEL_PRICING
from core.router import analyze_task_complexity

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "subagent_tracker", "backend", "tracker.db")

MODEL_CAPABILITIES: Dict[str, Dict[str, Any]] = {
    "gpt-4o": {"accuracy": 0.98, "tier": "high"},
    "claude-3-5-sonnet": {"accuracy": 0.99, "tier": "high"},
    "gpt-4o-mini": {"accuracy": 0.88, "tier": "medium"},
    "gemini-1.5-flash": {"accuracy": 0.85, "tier": "medium"},
    "llama3": {"accuracy": 0.80, "tier": "low"}
}

def get_historical_model_latencies() -> Dict[str, float]:
    """Retrieves empirical average latency per model from tracker database."""
    latencies = {}
    if not os.path.exists(DB_PATH):
        return latencies

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT model_name, AVG(execution_time_ms) FROM agentlog GROUP BY model_name")
        rows = cursor.fetchall()
        for model, avg_lat in rows:
            latencies[model.lower()] = round(avg_lat or 150.0, 1)
        conn.close()
    except Exception:
        pass
    return latencies

def select_optimal_model(
    prompt_text: str,
    max_budget_usd: Optional[float] = None,
    max_latency_ms: Optional[float] = None,
    preference: str = "balanced"  # 'cost', 'speed', 'quality', 'balanced'
) -> Dict[str, Any]:
    """
    Dynamic Multi-Criteria Model Selector Algorithm.
    Scores and selects the best LLM based on task complexity, estimated cost, 
    historical latency, and user budget/quality constraints.
    """
    complexity_tier, recommended = analyze_task_complexity(prompt_text)
    estimated_prompt_tokens = count_tokens(prompt_text)
    estimated_completion_tokens = 150  # Typical expected completion length
    
    historical_latencies = get_historical_model_latencies()

    candidates: List[Dict[str, Any]] = []

    for model_name, info in MODEL_CAPABILITIES.items():
        cost = calculate_cost(estimated_prompt_tokens, estimated_completion_tokens, model_name)
        lat = historical_latencies.get(model_name, 200.0)

        # Skip candidates exceeding budget
        if max_budget_usd is not None and cost > max_budget_usd:
            continue
        # Skip candidates exceeding latency limit
        if max_latency_ms is not None and lat > max_latency_ms:
            continue

        accuracy_score = info["accuracy"]
        cost_penalty = cost * 1000.0  # Normalized cost penalty
        latency_penalty = lat / 1000.0  # Normalized latency penalty

        if preference == "cost":
            score = (accuracy_score * 0.2) - (cost_penalty * 0.8)
        elif preference == "speed":
            score = (accuracy_score * 0.2) - (latency_penalty * 0.8)
        elif preference == "quality":
            score = (accuracy_score * 0.9) - (cost_penalty * 0.1)
        else: # balanced
            score = (accuracy_score * 0.5) - (cost_penalty * 0.3) - (latency_penalty * 0.2)

        candidates.append({
            "model_name": model_name,
            "score": round(score, 4),
            "estimated_cost_usd": cost,
            "historical_latency_ms": lat,
            "accuracy_rating": info["accuracy"],
            "tier": info["tier"]
        })

    # Sort candidates by score descending
    candidates.sort(key=lambda x: x["score"], reverse=True)

    if not candidates:
        # Fallback if strict constraints excluded all
        chosen = "gpt-4o-mini"
        justification = "Fallback model chosen as constraints excluded all candidates."
    else:
        chosen = candidates[0]["model_name"]
        justification = f"Selected '{chosen}' with score {candidates[0]['score']} based on '{preference}' preference for {complexity_tier}-complexity task."

    return {
        "selected_model": chosen,
        "complexity_tier": complexity_tier,
        "justification": justification,
        "top_candidates": candidates[:3]
    }
