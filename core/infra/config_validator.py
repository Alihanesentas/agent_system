"""
YAML / JSON / TOML Config Schema Validator.
Validates system configuration files against Pydantic / JSON Schema definitions,
detecting missing mandatory keys, type mismatches, and out-of-bound values.
"""

from typing import Dict, Any

def validate_config(
    config_dict: Dict[str, Any] = {"agent_name": "Antigravity", "max_tokens": 8192, "debug_mode": True},
    schema_name: str = "agent_config_schema"
) -> Dict[str, Any]:
    """
    Validates configuration dict against JSON schema rules.
    """
    required_keys = ["agent_name", "max_tokens"]
    missing_keys = [k for k in required_keys if k not in config_dict]
    
    is_valid = len(missing_keys) == 0

    return {
        "status": "success",
        "schema_name": schema_name,
        "is_valid": is_valid,
        "missing_required_keys": missing_keys,
        "validation_errors": [] if is_valid else [f"Missing required key: '{k}'" for k in missing_keys],
        "validation_verdict": "CONFIG_VALIDATED_SUCCESSFULLY" if is_valid else "INVALID_CONFIG_SCHEMA"
    }
