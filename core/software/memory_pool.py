"""
Static Fixed-Block Embedded Memory Pool Designer.
Calculates block size (bytes), alignment padding (32-bit / 64-bit), pool memory footprint,
and deterministic O(1) allocation/deallocation overhead for RTOS memory pools.
"""

import math
from typing import Dict, Any

def design_memory_pool(
    block_size_bytes: int = 64,
    num_blocks: int = 32,
    alignment_bytes: int = 4
) -> Dict[str, Any]:
    """
    Designs deterministic static memory pool with byte alignment.
    """
    # Aligned block size
    aligned_block_size = math.ceil(block_size_bytes / float(alignment_bytes)) * alignment_bytes
    
    payload_ram = aligned_block_size * num_blocks
    control_overhead_ram = num_blocks * 4  # 4 bytes free-list pointer per block
    total_pool_ram_bytes = payload_ram + control_overhead_ram

    c_code = f"""// Static Memory Pool Definition
#include <stdint.h>

#define POOL_BLOCK_SIZE {aligned_block_size}
#define POOL_NUM_BLOCKS {num_blocks}

typedef struct {{
    uint8_t memory_pool[POOL_NUM_BLOCKS * POOL_BLOCK_SIZE];
    void* free_list[POOL_NUM_BLOCKS];
    uint32_t free_count;
}} StaticMemoryPool_t;
"""

    return {
        "status": "success",
        "requested_block_size_bytes": block_size_bytes,
        "aligned_block_size_bytes": aligned_block_size,
        "num_blocks": num_blocks,
        "alignment_bytes": alignment_bytes,
        "payload_ram_bytes": payload_ram,
        "control_overhead_bytes": control_overhead_ram,
        "total_pool_ram_bytes": total_pool_ram_bytes,
        "alloc_dealloc_complexity": "O(1) Constant Time (Deterministic)",
        "c_pool_definition": c_code
    }
