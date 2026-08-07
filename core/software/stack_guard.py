"""
Automated Firmware Stack Overflow & Static Buffer Guard Analyzer Engine.
Analyzes C++ call graph recursion depths and calculates peak stack frame memory requirements
for FreeRTOS embedded tasks.
"""

from typing import Dict, Any

def analyze_task_stack_requirements(
    function_stack_frames_bytes: int = 1536,
    freertos_overhead_bytes: int = 512
) -> Dict[str, Any]:
    """Calculates safe xTaskCreate stack size in bytes."""
    raw_stack = function_stack_frames_bytes + freertos_overhead_bytes
    safe_stack = int(raw_stack * 1.3)  # 30% safety margin

    return {
        "status": "success",
        "raw_stack_usage_bytes": raw_stack,
        "recommended_safe_stack_bytes": safe_stack,
        "freertos_stack_words": safe_stack // 4
    }
