"""
MQTT Topic Hierarchy & QoS Config Generator.
Generates structured IoT MQTT topic trees, payload JSON schemas, and C/Python client configs.
"""

from typing import Dict, Any

def generate_mqtt_config(
    project_id: str = "smart_factory",
    device_type: str = "gateway",
    device_id: str = "node_01"
) -> Dict[str, Any]:
    """
    Generates structured MQTT topic paths and QoS settings.
    """
    base_prefix = f"v1/{project_id}/{device_type}/{device_id}"
    
    topics = {
        "telemetry_pub": {"topic": f"{base_prefix}/telemetry", "qos": 1, "retain": False, "desc": "Sensor readings JSON payload"},
        "status_pub": {"topic": f"{base_prefix}/status", "qos": 1, "retain": True, "desc": "Device online/offline & birth message"},
        "lwt_pub": {"topic": f"{base_prefix}/lwt", "qos": 1, "retain": True, "desc": "Last Will & Testament unexpected disconnect"},
        "command_sub": {"topic": f"{base_prefix}/cmd/+", "qos": 2, "retain": False, "desc": "Incoming control commands"},
        "config_sub": {"topic": f"{base_prefix}/config", "qos": 1, "retain": True, "desc": "Remote device parameter configuration"}
    }

    return {
        "status": "success",
        "project_id": project_id,
        "device_id": device_id,
        "base_prefix": base_prefix,
        "topics": topics,
        "recommended_keepalive_sec": 60,
        "clean_session": True
    }
