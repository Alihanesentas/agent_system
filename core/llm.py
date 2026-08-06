import os
import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any

# Load environment variables from .env if present
try:
    with open(os.path.join(os.path.dirname(__file__), "..", ".env"), "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
except Exception:
    pass

def call_openai_api(prompt: str, model_name: str = "gpt-4o", system_prompt: Optional[str] = None) -> str:
    """Calls OpenAI Chat Completions REST API."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.startswith("your_"):
        return f"[Simulated {model_name} Response]: Processed prompt '{prompt[:40]}...'"

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {"model": model_name, "messages": messages, "temperature": 0.2}
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            data = json.loads(res.read().decode('utf-8'))
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"OpenAI API Error ({model_name}): {str(e)}"

def call_anthropic_api(prompt: str, model_name: str = "claude-3-5-sonnet-20240620", system_prompt: Optional[str] = None) -> str:
    """Calls Anthropic Messages REST API."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key.startswith("your_"):
        return f"[Simulated {model_name} Response]: Processed prompt '{prompt[:40]}...'"

    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }
    payload = {
        "model": model_name,
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}]
    }
    if system_prompt:
        payload["system"] = system_prompt

    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            data = json.loads(res.read().decode('utf-8'))
            return data["content"][0]["text"].strip()
    except Exception as e:
        return f"Anthropic API Error ({model_name}): {str(e)}"

def call_gemini_api(prompt: str, model_name: str = "gemini-1.5-flash", system_prompt: Optional[str] = None) -> str:
    """Calls Google Gemini REST API."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key.startswith("your_"):
        return f"[Simulated {model_name} Response]: Processed prompt '{prompt[:40]}...'"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    full_text = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
    payload = {"contents": [{"parts": [{"text": full_text}]}]}

    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            data = json.loads(res.read().decode('utf-8'))
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        return f"Gemini API Error ({model_name}): {str(e)}"

def call_ollama_api(prompt: str, model_name: str = "llama3", system_prompt: Optional[str] = None) -> str:
    """Calls Local Ollama REST API (Free Offline Local Models)."""
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    url = f"{base_url}/api/generate"
    headers = {"Content-Type": "application/json"}
    
    full_prompt = f"System: {system_prompt}\nUser: {prompt}" if system_prompt else prompt
    payload = {"model": model_name, "prompt": full_prompt, "stream": False}

    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as res:
            data = json.loads(res.read().decode('utf-8'))
            return data.get("response", "").strip()
    except Exception as e:
        return f"[Simulated Local Ollama ({model_name})]: Local model response for '{prompt[:30]}...'"

def call_llm(prompt: str, model_name: str = "gpt-4o", system_prompt: Optional[str] = None) -> str:
    """
    Unified LLM Dispatcher. Routes requests to OpenAI, Anthropic, Gemini, or Ollama 
    based on the target model name.
    """
    m_lower = model_name.lower()

    if "gpt" in m_lower or "openai" in m_lower:
        return call_openai_api(prompt, model_name=model_name, system_prompt=system_prompt)
    elif "claude" in m_lower or "anthropic" in m_lower:
        return call_anthropic_api(prompt, model_name=model_name, system_prompt=system_prompt)
    elif "gemini" in m_lower or "google" in m_lower:
        return call_gemini_api(prompt, model_name=model_name, system_prompt=system_prompt)
    elif "ollama" in m_lower or "llama" in m_lower or "qwen" in m_lower or "deepseek" in m_lower:
        return call_ollama_api(prompt, model_name=model_name, system_prompt=system_prompt)
    else:
        # Default fallback dispatcher
        return call_openai_api(prompt, model_name=model_name, system_prompt=system_prompt)
