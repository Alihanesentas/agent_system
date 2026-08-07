from typing import Dict, Any, Tuple
import re

HIGH_COMPLEXITY_KEYWORDS = [
    "architecture", "refactor whole project", "security audit", 
    "distributed system", "concurrency", "algorithm optimization", 
    "multi-agent protocol", "compiler", "ast transform"
]

LOW_COMPLEXITY_KEYWORDS = [
    "format", "clean whitespace", "summarize", "list files", 
    "rename", "status check", "simple print", "fix typo"
]

def analyze_task_complexity(prompt: str) -> Tuple[str, str]:
    """
    Analyzes prompt text complexity and routes to the optimal LLM tier:
    - 'low'    -> gpt-4o-mini / gemini-1.5-flash (Cost reduction: ~95%)
    - 'medium' -> gpt-4o-mini / gpt-4o (Cost reduction: ~70%)
    - 'high'   -> gpt-4o / claude-3-5-sonnet (Flagship accuracy)
    """
    prompt_lower = prompt.lower()
    length = len(prompt)

    # 1. Low complexity matching
    for kw in LOW_COMPLEXITY_KEYWORDS:
        if kw in prompt_lower and length < 200:
            return "low", "gpt-4o-mini"

    # 2. High complexity matching
    for kw in HIGH_COMPLEXITY_KEYWORDS:
        if kw in prompt_lower or length > 800:
            return "high", "gpt-4o"

    # Default medium tier
    return "medium", "gpt-4o-mini"

def route_agent_task(prompt: str, user_selected_model: str = None) -> Dict[str, Any]:
    """
    Intelligent Model Cascading Router. Automatically selects the most cost-efficient 
    model tier based on task complexity.
    """
    complexity, recommended_model = analyze_task_complexity(prompt)
    chosen_model = user_selected_model or recommended_model

    est_savings = "95%" if recommended_model == "gpt-4o-mini" else "0%"

    return {
        "complexity_tier": complexity,
        "recommended_model": recommended_model,
        "chosen_model": chosen_model,
        "estimated_cost_savings": est_savings
    }
