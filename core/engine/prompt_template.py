"""
Version-Controlled Prompt Template Engine.
Renders parameter-injected LLM system prompts using key-value substitutions.
"""

from typing import Dict, Any

DEFAULT_TEMPLATES = {
    "electronics_engineer": "You are an expert Electronics Engineer specializing in PCB design for {mcu}. Standard voltage is {voltage}V.",
    "firmware_engineer": "You are a C/C++ Firmware Architect writing RTOS code for {platform} with {memory_kb}KB RAM limit.",
    "mechanical_engineer": "You are a 3D CAD Engineer generating OpenSCAD enclosures with {clearance_mm}mm tolerance."
}

def render_prompt_template(
    template_name: str = "electronics_engineer",
    variables: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Renders versioned prompt template with dynamic variable injection.
    """
    if not variables:
        variables = {"mcu": "ESP32-S3", "voltage": 3.3, "platform": "ESP-IDF", "memory_kb": 512, "clearance_mm": 0.5}

    raw_template = DEFAULT_TEMPLATES.get(template_name, "Task: {task}")
    
    rendered = raw_template
    for k, v in variables.items():
        placeholder = f"{{{k}}}"
        if placeholder in rendered:
            rendered = rendered.replace(placeholder, str(v))

    return {
        "status": "success",
        "template_name": template_name,
        "variables_injected": len(variables),
        "rendered_prompt": rendered
    }
