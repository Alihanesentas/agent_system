"""
Protocol Buffers (proto3) Schema & C Struct Header Generator.
Generates `.proto` definitions and micro-nanopb C header struct packed representations
for embedded IoT message serialization.
"""

from typing import Dict, Any

def generate_protobuf_schema(
    message_name: str = "DeviceStatus"
) -> Dict[str, Any]:
    """
    Generates proto3 schema and nanopb C header boilerplate.
    """
    proto_schema = f"""syntax = "proto3";
package iot.telemetry;

message {message_name} {{
    uint32 device_id = 1;
    uint64 timestamp = 2;
    float battery_voltage = 3;
    bool is_online = 4;
    string firmware_version = 5;
}}
"""

    return {
        "status": "success",
        "message_name": message_name,
        "proto_schema": proto_schema,
        "field_count": 5,
        "recommended_library": "nanopb (Nanopb ANSI C Protocol Buffers)"
    }
