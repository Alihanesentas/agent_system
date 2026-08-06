import json
import re
from typing import Dict, Any, Tuple
from subagent_tracker.backend.tracker import count_tokens

def extract_json_payload(text: str) -> Dict[str, Any]:
    """
    Extracts structured JSON payload from an LLM response string.
    Supports markdown ```json blocks and raw JSON substrings.
    """
    if not text:
        return {}

    # 1. Search for fenced ```json ... ``` blocks
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # 2. Search for object braces { ... }
    match_brace = re.search(r"\{[\s\S]*\}", text)
    if match_brace:
        try:
            return json.loads(match_brace.group(0))
        except json.JSONDecodeError:
            pass

    # Fallback envelope
    return {"raw_output": text.strip()}

def format_structured_agent_response(
    agent_name: str, 
    action: str, 
    result_data: Any, 
    status: str = "success"
) -> Tuple[str, Dict[str, Any]]:
    """
    Formats an agent response into a token-efficient, compact JSON string.
    Reduces completion tokens by eliminating conversational fluff.
    """
    payload = {
        "agent": agent_name,
        "status": status,
        "action": action,
        "result": result_data
    }
    json_str = json.dumps(payload, separators=(',', ':'))
    raw_verbose_fluff = f"Hello! As the {agent_name} agent, I have successfully executed your requested action '{action}'. Here is the resulting output data: {result_data}. Please let me know if you need anything else!"
    
    tokens_json = count_tokens(json_str)
    tokens_fluff = count_tokens(raw_verbose_fluff)
    saved = max(0, tokens_fluff - tokens_json)

    metrics = {
        "json_tokens": tokens_json,
        "verbose_tokens": tokens_fluff,
        "tokens_saved": saved,
        "completion_token_reduction_percent": round((saved / tokens_fluff * 100), 1) if tokens_fluff > 0 else 0.0
    }

    return json_str, metrics
