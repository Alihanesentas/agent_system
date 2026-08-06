import re
from typing import Tuple, Dict, Any
from subagent_tracker.backend.tracker import count_tokens, calculate_cost

DEFAULT_FILLER_PATTERNS = [
    r"\bcould you please\b",
    r"\bcan you please\b",
    r"\bi would like you to\b",
    r"\bi want you to kindly\b",
    r"\bplease make sure to\b",
    r"\bplease ensure that\b",
    r"\bas an ai assistant\b",
    r"\bfor this task\b"
]

def compress_prompt(prompt_text: str, model_name: str = "gpt-4o") -> Tuple[str, Dict[str, Any]]:
    """
    Compresses an LLM prompt by removing redundant conversational filler, 
    extra whitespace, and duplicate instructions while preserving code blocks and semantics.
    
    Returns:
        (compressed_text, metrics_dict)
    """
    if not prompt_text:
        return prompt_text, {
            "original_tokens": 0,
            "compressed_tokens": 0,
            "tokens_saved": 0,
            "savings_percent": 0.0
        }

    original_tokens = count_tokens(prompt_text, model_name)

    # Protect fenced code blocks during compression
    code_blocks = []
    def save_code_block(match):
        code_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"

    # Replace ``` code blocks ``` with placeholders
    text = re.sub(r"```[\s\S]*?```", save_code_block, prompt_text)

    # 1. Remove conversational filler phrases (case-insensitive)
    for pattern in DEFAULT_FILLER_PATTERNS:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    # 2. Collapse multiple spaces and blank lines
    lines = [line.strip() for line in text.splitlines()]
    
    # 3. Deduplicate consecutive identical lines
    deduped_lines = []
    for line in lines:
        if line and (not deduped_lines or line != deduped_lines[-1]):
            deduped_lines.append(line)

    compressed_text = "\n".join(deduped_lines)

    # Restore fenced code blocks
    for idx, block in enumerate(code_blocks):
        compressed_text = compressed_text.replace(f"__CODE_BLOCK_{idx}__", block)

    compressed_tokens = count_tokens(compressed_text, model_name)
    tokens_saved = max(0, original_tokens - compressed_tokens)
    savings_percent = round((tokens_saved / original_tokens * 100), 1) if original_tokens > 0 else 0.0

    metrics = {
        "original_tokens": original_tokens,
        "compressed_tokens": compressed_tokens,
        "tokens_saved": tokens_saved,
        "savings_percent": savings_percent,
        "original_cost": calculate_cost(original_tokens, 0, model_name),
        "compressed_cost": calculate_cost(compressed_tokens, 0, model_name),
        "cost_saved_usd": round(calculate_cost(original_tokens, 0, model_name) - calculate_cost(compressed_tokens, 0, model_name), 6)
    }

    return compressed_text, metrics
