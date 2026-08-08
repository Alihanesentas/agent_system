"""
Lock-Free Circular Ring Buffer Sizer & C Code Generator.
Calculates power-of-two buffer capacity, index masking efficiency (`head & (CAPACITY - 1)`),
RAM memory usage, and thread-safe lock-free C header code for UART/SPI DMA buffers.
"""

from typing import Dict, Any

def design_ring_buffer(
    requested_capacity: int = 500,
    element_size_bytes: int = 1
) -> Dict[str, Any]:
    """
    Calculates power-of-two ring buffer size and C code.
    """
    # Next power of 2
    capacity = 1
    while capacity < requested_capacity:
        capacity <<= 1
        
    mask = capacity - 1
    total_ram_bytes = capacity * element_size_bytes
    
    c_header = f"""// Lock-Free Circular Ring Buffer (Power of 2 Capacity: {capacity})
#include <stdint.h>
#include <stdbool.h>

#define RING_BUF_CAPACITY {capacity}
#define RING_BUF_MASK {mask}

typedef struct {{
    uint8_t buffer[RING_BUF_CAPACITY];
    volatile uint32_t head;
    volatile uint32_t tail;
}} RingBuffer_t;

static inline bool ring_buf_push(RingBuffer_t *rb, uint8_t data) {{
    uint32_t next = (rb->head + 1) & RING_BUF_MASK;
    if (next == rb->tail) return false; // Full
    rb->buffer[rb->head & RING_BUF_MASK] = data;
    rb->head = next;
    return true;
}}
"""

    return {
        "status": "success",
        "requested_capacity": requested_capacity,
        "power_of_two_capacity": capacity,
        "bitmask_hex": hex(mask),
        "element_size_bytes": element_size_bytes,
        "total_ram_bytes": total_ram_bytes,
        "thread_safety": "Lock-Free Single Producer Single Consumer (SPSC)",
        "c_ring_buffer_code": c_header
    }
