# agent_system/core/runner.py
import time
import requests
import functools
from typing import Dict, Any, Callable, Optional

from core.optimizer import compress_prompt
from core.cache import find_cached_response, store_in_cache
from core.llm import call_llm
from core.rag import build_rag_context

TRACKER_API_URL = "http://127.0.0.1:8000/api/log"

def log_agent_activity(
    agent_name: str, 
    model_name: str, 
    input_text: str, 
    output_text: str,
    execution_time_ms: float = 0.0,
    session_id: Optional[int] = None,
    status: str = "success"
) -> Dict[str, Any]:
    """Subagent token ve zamanlama kullanımını tracker modülüne bildirir."""
    try:
        payload = {
            "agent_name": agent_name,
            "model_name": model_name,
            "input_text": input_text,
            "output_text": output_text,
            "execution_time_ms": execution_time_ms,
            "session_id": session_id,
            "status": status
        }
        res = requests.post(TRACKER_API_URL, json=payload, timeout=3)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"⚠️ Tracker servisine log gönderilemedi: {e}")
    return {}

def trace_agent(agent_name: str, model_name: str = "gpt-4o", session_id: Optional[int] = None):
    """
    Decorator to automatically trace execution latency, token counts, 
    and log subagent activity to the tracker service.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            input_repr = f"Args: {args}, Kwargs: {kwargs}"
            status = "success"
            output_text = ""
            try:
                result = func(*args, **kwargs)
                output_text = str(result)
                return result
            except Exception as e:
                status = "error"
                output_text = f"Error: {str(e)}"
                raise e
            finally:
                elapsed_ms = round((time.time() - start_time) * 1000, 2)
                log_agent_activity(
                    agent_name=agent_name,
                    model_name=model_name,
                    input_text=input_repr,
                    output_text=output_text,
                    execution_time_ms=elapsed_ms,
                    session_id=session_id,
                    status=status
                )
        return wrapper
    return decorator

def run_agent_task(
    agent_name: str,
    user_prompt: str,
    model_name: str = "gpt-4o",
    system_prompt: Optional[str] = None,
    session_id: Optional[int] = None,
    use_cache: bool = True,
    optimize_prompt: bool = False,
    use_rag: bool = True,
    agent_fn: Optional[Callable[[str], str]] = None
) -> str:
    """
    Executes an agent task with live LLM API Integration, Semantic Caching, 
    and Prompt Optimization. Telemetry logged automatically.
    """
    input_to_process = f"System: {system_prompt}\nUser: {user_prompt}" if system_prompt else user_prompt

    # 1. Semantic Cache Lookup
    if use_cache:
        cached = find_cached_response(user_prompt, agent_name=agent_name)
        if cached:
            print(f"🎯 [Semantic Cache HIT!]: (Similarity: {cached['similarity']*100:.1f}%) Returning instant cached response.")
            output_text = f"[CACHE HIT] {cached['response']}"
            log_agent_activity(
                agent_name=agent_name,
                model_name=cached['model_name'],
                input_text=f"[CACHE HIT] {input_to_process}",
                output_text=output_text,
                execution_time_ms=0.5,
                session_id=session_id,
                status="cache_hit"
            )
            return cached['response']

    # 2. RAG Context Injection
    if use_rag:
        rag_context = build_rag_context(user_prompt, n_results=3, max_context_chars=3000)
        if rag_context:
            input_to_process = rag_context + input_to_process
            print(f"📚 [RAG]: Injected {len(rag_context)} chars of retrieved context from indexed documents.")

    # 3. Optional Prompt Optimization
    if optimize_prompt:
        compressed_input, metrics = compress_prompt(input_to_process, model_name)
        print(f"⚡ [Token Optimizer]: Compressed prompt from {metrics['original_tokens']} -> {metrics['compressed_tokens']} tokens ({metrics['savings_percent']}% savings)")
        input_to_process = compressed_input

    start_time = time.time()
    status = "success"
    
    if agent_fn:
        try:
            output = agent_fn(input_to_process)
        except Exception as e:
            status = "error"
            output = f"Execution Error: {str(e)}"
    else:
        # Unified Live LLM API Dispatcher (OpenAI, Anthropic, Gemini, Ollama)
        try:
            output = call_llm(input_to_process, model_name=model_name, system_prompt=system_prompt)
        except Exception as e:
            status = "error"
            output = f"LLM API Error: {str(e)}"
    
    elapsed_ms = round((time.time() - start_time) * 1000, 2)
    
    # Store in Semantic Cache for future identical/similar calls
    if use_cache and status == "success":
        store_in_cache(user_prompt, output, agent_name=agent_name, model_name=model_name)

    log_agent_activity(
        agent_name=agent_name,
        model_name=model_name,
        input_text=input_to_process,
        output_text=output,
        execution_time_ms=elapsed_ms,
        session_id=session_id,
        status=status
    )
    
    return output