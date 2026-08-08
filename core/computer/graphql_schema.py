"""
GraphQL Schema Definition & Resolver Generator.
Generates GraphQL type definitions (SDL), query/mutation schemas, and Node.js / Python resolver stubs.
"""

from typing import Dict, Any, List

def generate_graphql_schema(
    type_name: str = "TelemetryReading"
) -> Dict[str, Any]:
    """
    Generates GraphQL SDL schema and resolvers.
    """
    sdl_schema = f"""# Auto-generated GraphQL SDL Schema for {type_name}
type {type_name} {{
  id: ID!
  deviceId: String!
  temperature: Float
  humidity: Float
  timestamp: String!
}}

input Create{type_name}Input {{
  deviceId: String!
  temperature: Float
  humidity: Float
}}

type Query {{
  get{type_name}(id: ID!): {type_name}
  list{type_name}s(limit: Int = 10): [{type_name}!]!
}}

type Mutation {{
  create{type_name}(input: Create{type_name}Input!): {type_name}!
}}
"""

    return {
        "status": "success",
        "type_name": type_name,
        "graphql_sdl": sdl_schema,
        "queries_count": 2,
        "mutations_count": 1
    }
