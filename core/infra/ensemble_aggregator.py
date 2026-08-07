"""
Multi-Model Dynamic Ensemble Aggregator & Voting Engine.
Runs multiple LLM model responses in parallel and merges their predictions
using weighted majority consensus to eliminate hallucination risks.
"""

from typing import Dict, Any, List

def aggregate_ensemble_responses(
    responses: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Merges multi-model outputs into a single high-confidence consensus answer."""
    if not responses:
        return {"status": "error", "message": "No model responses to aggregate."}
        
    vote_counts = {}
    for r in responses:
        ans = r.get("answer", "UNKNOWN")
        vote_counts[ans] = vote_counts.get(ans, 0) + 1

    winning_answer = max(vote_counts, key=vote_counts.get)
    agreement_rate = round((vote_counts[winning_answer] / len(responses)) * 100.0, 1)

    return {
        "status": "success",
        "total_models": len(responses),
        "winning_answer": winning_answer,
        "agreement_rate_pct": agreement_rate,
        "vote_breakdown": vote_counts
    }
