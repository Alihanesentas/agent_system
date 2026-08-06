# agent_system/core/runner.py
import time
import requests
import functools
from typing import Dict, Any, Callable, Optional

from core.optimizer import compress_prompt

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
    optimize_prompt: bool = False,
    agent_fn: Optional[Callable[[str], str]] = None
) -> str:
    """
    Executes an agent task, measuring timing and sending telemetry data to the backend.
    Supports optional prompt optimization to reduce token consumption.
    """
    input_to_process = f"System: {system_prompt}\nUser: {user_prompt}" if system_prompt else user_prompt
    
    if optimize_prompt:
        compressed_input, metrics = compress_prompt(input_to_process, model_name)
        print(f"⚡ [Token Optimizer]: Prompt compressed from {metrics['original_tokens']} -> {metrics['compressed_tokens']} tokens ({metrics['savings_percent']}% savings)")
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
        # Default mock simulation for demonstration / benchmarking
        output = f"[{agent_name} Response ({model_name})]: Processed task for prompt: '{user_prompt[:40]}...'"
    
    elapsed_ms = round((time.time() - start_time) * 1000, 2)
    
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