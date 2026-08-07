"""
LLM Prompt System Message Personalization Engine.
Dynamically builds specialized engineer prompt context based on domain tags,
user profile constraints, and target hardware architecture (/prompt-builder).
"""

from typing import Dict, Any, List

def build_personalized_engineer_prompt(
    agent_role: str = "Electronics Engineer",
    target_mcu: str = "ESP32-S3",
    domain_tags: List[str] = ["PCB", "KiCad", "EMC"]
) -> Dict[str, Any]:
    """Builds tailored system prompt context for sub-agent execution."""
    prompt_context = f"You are an expert {agent_role} specializing in {target_mcu} design. Active domains: {', '.join(domain_tags)}."
    
    return {
        "status": "success",
        "agent_role": agent_role,
        "target_mcu": target_mcu,
        "domain_tags": domain_tags,
        "generated_system_prompt": prompt_context
    }
