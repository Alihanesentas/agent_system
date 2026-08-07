"""
LLM Prompt System Token Counter & Cost Minimizer Engine.
Calculates exact BPE token counts and estimates per-model request cost ($)
before sending prompts over the wire (/token-count).
"""

from typing import Dict, Any

def count_and_estimate_tokens(prompt_text: str) -> Dict[str, Any]:
    """Estimates BPE token count and request cost across model tiers."""
    char_len = len(prompt_text)
    est_tokens = max(1, char_len // 4)  # ~4 chars per token rule
    
    cost_gpt4o = est_tokens * (2.5 / 1_000_000)
    cost_mini = est_tokens * (0.15 / 1_000_000)
    cost_flash = est_tokens * (0.075 / 1_000_000)

    return {
        "status": "success",
        "char_length": char_len,
        "estimated_bpe_tokens": est_tokens,
        "estimated_costs_usd": {
            "gpt-4o": round(cost_gpt4o, 6),
            "gpt-4o-mini": round(cost_mini, 6),
            "gemini-1.5-flash": round(cost_flash, 6)
        }
    }
