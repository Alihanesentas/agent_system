"""
Personalized Engineer Profile Manager.
Stores user's hardware preferences, preferred MCU families, CAD tools, 
and engineering constraints to personalize all agent prompts automatically.
"""

import os
import json
from typing import Dict, Any, Optional

PROFILE_FILE = os.path.join(os.path.dirname(__file__), "..", "user_profile.json")

DEFAULT_PROFILE = {
    "user_name": "Alihan",
    "primary_disciplines": ["Embedded Systems", "Electronics", "Mechanical CAD", "Edge AI"],
    "preferred_mcu": "ESP32-S3",
    "preferred_cad_tool": "OpenSCAD",
    "preferred_language": "C++ / Python",
    "default_i2c_sda": "GPIO21",
    "default_i2c_scl": "GPIO22",
    "default_baudrate": 115200,
    "custom_engineering_rules": [
        "Always use 4.7k pull-up resistors on I2C bus lines.",
        "Add 100nF ceramic decoupling capacitor next to VCC pins.",
        "Enforce strict INT8 quantization for Edge AI models on ESP32-S3."
    ]
}

def load_user_profile() -> Dict[str, Any]:
    """Loads personalized user engineering profile."""
    if not os.path.exists(PROFILE_FILE):
        save_user_profile(DEFAULT_PROFILE)
        return DEFAULT_PROFILE

    try:
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_PROFILE

def save_user_profile(profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """Saves personalized user profile to user_profile.json."""
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profile_data, f, indent=2)
    return {"status": "saved", "profile": profile_data}

def build_personalized_system_prompt(base_prompt: str) -> str:
    """Injects personalized engineer preferences into base agent system prompts."""
    profile = load_user_profile()
    rules = "\n".join([f"  • {r}" for r in profile.get("custom_engineering_rules", [])])

    personalized = (
        f"=== PERSONALIZED ENGINEER CONTEXT ({profile['user_name']}) ===\n"
        f"Primary Disciplines: {', '.join(profile['primary_disciplines'])}\n"
        f"Preferred MCU: {profile['preferred_mcu']} | CAD: {profile['preferred_cad_tool']}\n"
        f"Custom Engineering Rules:\n{rules}\n"
        f"=== END PERSONALIZED CONTEXT ===\n\n"
        f"{base_prompt}"
    )
    return personalized
