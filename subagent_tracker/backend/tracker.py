import tiktoken
from typing import Tuple, Dict

# Standard pricing estimates in USD per 1,000 tokens
MODEL_PRICING: Dict[str, Dict[str, float]] = {
    "gpt-4o": {"input": 0.0025 / 1000, "output": 0.0100 / 1000},
    "gpt-4o-mini": {"input": 0.00015 / 1000, "output": 0.0006 / 1000},
    "gpt-4": {"input": 0.03 / 1000, "output": 0.06 / 1000},
    "gpt-3.5-turbo": {"input": 0.0015 / 1000, "output": 0.0020 / 1000},
    "claude-3-5-sonnet": {"input": 0.0030 / 1000, "output": 0.0150 / 1000},
    "claude-3-haiku": {"input": 0.00025 / 1000, "output": 0.00125 / 1000},
    "gemini-1.5-flash": {"input": 0.000075 / 1000, "output": 0.0003 / 1000},
    "gemini-1.5-pro": {"input": 0.00125 / 1000, "output": 0.0050 / 1000},
    "gemini-3.6-flash": {"input": 0.000075 / 1000, "output": 0.0003 / 1000},
    "default": {"input": 0.0015 / 1000, "output": 0.0020 / 1000}
}

def count_tokens(text: str, model_name: str = "gpt-4o") -> int:
    """Counts tokens in a given text using tiktoken or fallback approximation."""
    if not text:
        return 0
    try:
        try:
            encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except Exception:
        # Fallback estimation: ~4 characters per token
        return max(1, len(text) // 4)

def calculate_cost(prompt_tokens: int, completion_tokens: int, model_name: str = "gpt-4o") -> float:
    """Calculates estimated cost in USD based on prompt and completion token counts."""
    pricing = MODEL_PRICING.get(model_name.lower())
    if not pricing:
        # Check partial match
        for key in MODEL_PRICING:
            if key in model_name.lower():
                pricing = MODEL_PRICING[key]
                break
    if not pricing:
        pricing = MODEL_PRICING["default"]

    input_cost = prompt_tokens * pricing["input"]
    output_cost = completion_tokens * pricing["output"]
    return round(input_cost + output_cost, 6)

def process_agent_activity(
    input_text: str, 
    output_text: str, 
    model_name: str = "gpt-4o"
) -> Tuple[int, int, int, float]:
    """Helper to compute prompt tokens, completion tokens, total tokens, and estimated cost."""
    prompt_tokens = count_tokens(input_text, model_name)
    completion_tokens = count_tokens(output_text, model_name)
    total_tokens = prompt_tokens + completion_tokens
    cost = calculate_cost(prompt_tokens, completion_tokens, model_name)
    
    return prompt_tokens, completion_tokens, total_tokens, cost
