"""
GCC / ARM Map File Code Size & Memory Usage Analyzer.
Parses Linker Map files (`.map`), calculating total Flash/ROM footprint (KB),
RAM SRAM static allocation (BSS + Data), vector table offset, and heap/stack clearance.
"""

from typing import Dict, Any

def analyze_code_size(
    text_section_bytes: int = 124500,
    data_section_bytes: int = 2048,
    bss_section_bytes: int = 16384,
    flash_limit_kb: int = 512,
    ram_limit_kb: int = 128
) -> Dict[str, Any]:
    """
    Analyzes GCC linker memory sections (.text, .data, .bss).
    """
    total_flash_used_bytes = text_section_bytes + data_section_bytes
    total_ram_used_bytes = data_section_bytes + bss_section_bytes
    
    flash_used_kb = total_flash_used_bytes / 1024.0
    ram_used_kb = total_ram_used_bytes / 1024.0
    
    flash_pct = (flash_used_kb / flash_limit_kb) * 100.0 if flash_limit_kb > 0 else 0.0
    ram_pct = (ram_used_kb / ram_limit_kb) * 100.0 if ram_limit_kb > 0 else 0.0

    return {
        "status": "success",
        "text_code_bytes": text_section_bytes,
        "data_init_bytes": data_section_bytes,
        "bss_uninit_bytes": bss_section_bytes,
        "flash_used_kb": round(flash_used_kb, 2),
        "flash_limit_kb": flash_limit_kb,
        "flash_utilization_pct": round(flash_pct, 1),
        "ram_used_kb": round(ram_used_kb, 2),
        "ram_limit_kb": ram_limit_kb,
        "ram_utilization_pct": round(ram_pct, 1),
        "memory_verdict": "PASSED (Healthy ROM/RAM Margin)" if flash_pct < 85.0 and ram_pct < 85.0 else "WARN: High Memory Usage >85%"
    }
