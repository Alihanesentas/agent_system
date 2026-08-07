"""
Microservices gRPC Protobuf & Event Bus Generator Engine.
Generates gRPC .proto service definitions and RabbitMQ / Kafka event bus schemas.
"""

from typing import Dict, Any

def generate_microservice_proto(service_name: str = "UserService") -> Dict[str, Any]:
    """Generates gRPC proto3 definition."""
    proto_code = f"""syntax = "proto3";

package {service_name.lower()};

service {service_name} {{
  rpc GetUser (UserRequest) returns (UserResponse);
}}

message UserRequest {{
  string user_id = 1;
}}

message UserResponse {{
  string user_id = 1;
  string email = 2;
  string name = 3;
}}
"""
    return {
        "status": "success",
        "service_name": service_name,
        "proto_code": proto_code
    }
