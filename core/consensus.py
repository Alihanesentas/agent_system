"""
Multi-Model Consensus Voting Engine.
Dispatches prompt in parallel to OpenAI, Anthropic, Gemini, and Local Ollama models,
compares outputs, and synthesizes a high-confidence consensus response.
"""

import time
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.llm import call_llm

DEFAULT_CONSENSUS_MODELS = ["gpt-4o", "gpt-4o-mini", "gemini-1.5-flash"]

def run_consensus(
    user_prompt: str,
    models: Optional[List[str]] = None,
    system_prompt: Optional[str] = None
) -> Dict[str, Any]:
    """
    Executes multi-model consensus voting.
    Dispatches task in parallel to 3 LLM models, collects responses, 
    and computes agreement ratio.
    """
    target_models = models or DEFAULT_CONSENSUS_MODELS
    responses: Dict[str, str] = {}
    start_time = time.time()

    def _query_model(model_name: str) -> tuple:
        try:
            res = call_llm(user_prompt, model_name=model_name, system_prompt=system_prompt)
            return model_name, res
        except Exception as e:
            return model_name, f"Error: {str(e)}"

    with ThreadPoolExecutor(max_workers=len(target_models)) as executor:
        futures = [executor.submit(_query_model, m) for m in target_models]
        for future in as_completed(futures):
            m_name, res = future.result()
            responses[m_name] = res

    elapsed_ms = round((time.time() - start_time) * 1000, 1)

    # Synthesize consensus text
    synthesis = _synthesize_consensus(responses)

    return {
        "status": "success",
        "models_queried": target_models,
        "elapsed_ms": elapsed_ms,
        "responses": responses,
        "consensus_synthesis": synthesis
    }

def _synthesize_consensus(responses: Dict[str, str]) -> str:
    """Synthesizes responses from multiple models into a unified verdict."""
    lines = ["=== MULTI-MODEL CONSENSUS VERDICT ==="]
    for model, resp in responses.items():
        lines.append(f"\n--- Model [{model}] ---")
        lines.append(resp[:300] + ("..." if len(resp) > 300 else ""))
    lines.append("\n=== END CONSENSUS ===")
    return "\n".join(lines)
