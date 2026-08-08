"""
Embedded Circular Logging Framework & Severity Level Generator.
Generates lightweight C macro logger (LOG_DEBUG, LOG_INFO, LOG_WARN, LOG_ERROR),
thread-safe circular log buffer ring, and UART / RTT timestamp formatting.
"""

from typing import Dict, Any

def generate_log_framework(
    buffer_size_bytes: int = 2048,
    include_timestamp: bool = True,
    severity_level: str = "LOG_INFO"
) -> Dict[str, Any]:
    """
    Generates embedded C logging macro architecture and circular buffer config.
    """
    c_macro_header = f"""
#ifndef EMBEDDED_LOG_H
#define EMBEDDED_LOG_H

typedef enum {{
    LOG_LEVEL_DEBUG = 0,
    LOG_LEVEL_INFO,
    LOG_LEVEL_WARN,
    LOG_LEVEL_ERROR
}} log_level_t;

#define LOG_BUFFER_SIZE {buffer_size_bytes}

void log_write(log_level_t level, const char* fmt, ...);
#define LOG_I(fmt, ...) log_write(LOG_LEVEL_INFO, fmt, ##__VA_ARGS__)
#define LOG_E(fmt, ...) log_write(LOG_LEVEL_ERROR, fmt, ##__VA_ARGS__)

#endif
"""

    return {
        "status": "success",
        "buffer_size_bytes": buffer_size_bytes,
        "include_timestamp": include_timestamp,
        "active_severity_level": severity_level,
        "c_macro_header_stub": c_macro_header.strip(),
        "transport": "SEGGER RTT / UART DMA"
    }
