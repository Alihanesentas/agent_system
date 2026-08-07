"""
Hardware Knowledge Graph Engine.
Builds an interconnected graph mapping microcontrollers, sensors, pinouts,
IC datasheets, and user project rules for instant relational knowledge retrieval.
"""

from typing import Dict, Any, List, Optional

class HardwareKnowledgeGraph:
    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, Any]] = []
        self._seed_graph()

    def _seed_graph(self):
        # Microcontrollers
        self.nodes["ESP32-S3"] = {"type": "MCU", "architecture": "LX7 Dual-Core 240MHz", "vcc": "3.3V"}
        self.nodes["STM32F401"] = {"type": "MCU", "architecture": "Cortex-M4 84MHz", "vcc": "3.3V"}
        
        # Sensors
        self.nodes["BME280"] = {"type": "Sensor", "interface": "I2C/SPI", "address": "0x76", "voltage": "3.3V"}
        self.nodes["MPU6050"] = {"type": "Sensor", "interface": "I2C", "address": "0x68", "voltage": "3.3V"}

        # Edges
        self.edges.append({"source": "ESP32-S3", "target": "BME280", "relation": "COMPATIBLE_I2C", "pins": "GPIO21/GPIO22"})
        self.edges.append({"source": "ESP32-S3", "target": "MPU6050", "relation": "COMPATIBLE_I2C", "pins": "GPIO21/GPIO22"})

    def query_graph(self, query: str) -> Dict[str, Any]:
        """Queries the relational graph for components and interfaces."""
        query_upper = query.upper()
        matching_nodes = {k: v for k, v in self.nodes.items() if query_upper in k.upper()}
        matching_edges = [e for e in self.edges if query_upper in e["source"].upper() or query_upper in e["target"].upper()]

        return {
            "status": "success",
            "query": query,
            "matching_components_count": len(matching_nodes),
            "matching_relationships_count": len(matching_edges),
            "nodes": matching_nodes,
            "relationships": matching_edges
        }

global_knowledge_graph = HardwareKnowledgeGraph()
