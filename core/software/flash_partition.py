"""
C++ Memory Footprint & Flash Partition Layout Visualizer Engine.
Visualizes ESP32/STM32 partition tables (nvs, otadata, app0, app1, spiffs) and SRAM allocations.
"""

from typing import Dict, Any, List

def calculate_flash_partitions(flash_size_mb: int = 8) -> Dict[str, Any]:
    """Calculates partition sizes for 4MB / 8MB / 16MB flash ICs."""
    total_kb = flash_size_mb * 1024
    
    partitions = [
        {"name": "nvs", "type": "data", "subtype": "nvs", "offset": "0x9000", "size_kb": 20},
        {"name": "otadata", "type": "data", "subtype": "ota", "offset": "0xe000", "size_kb": 8},
        {"name": "app0", "type": "app", "subtype": "ota_0", "offset": "0x10000", "size_kb": 3072},
        {"name": "app1", "type": "app", "subtype": "ota_1", "offset": "0x310000", "size_kb": 3072},
        {"name": "spiffs", "type": "data", "subtype": "spiffs", "offset": "0x610000", "size_kb": total_kb - 6172}
    ]

    return {
        "status": "success",
        "total_flash_mb": flash_size_mb,
        "total_flash_kb": total_kb,
        "partitions": partitions
    }
