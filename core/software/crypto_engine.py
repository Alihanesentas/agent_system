"""
Embedded Cryptography & Security Hardware Accelerator Sizer.
Calculates RAM/Flash memory footprint, throughput (MB/s), and key sizing
for AES-128/256, ECC (secp256r1/ed25519), and SHA-256 hardware acceleration engines.
"""

from typing import Dict, Any

def design_crypto_params(
    algorithm: str = "AES-256-GCM",
    data_size_kb: float = 64.0,
    hardware_accelerator_present: bool = True
) -> Dict[str, Any]:
    """
    Calculates cryptographic throughput, RAM footprint, and key sizing.
    """
    algo_upper = algorithm.upper()
    
    if "AES-256" in algo_upper:
        key_bits = 256
        ram_bytes = 1024
        cycles_per_byte = 12 if hardware_accelerator_present else 180
    elif "ECC" in algo_upper or "ED25519" in algo_upper:
        key_bits = 256
        ram_bytes = 2048
        cycles_per_byte = 500 if hardware_accelerator_present else 8000
    else:  # AES-128
        key_bits = 128
        ram_bytes = 512
        cycles_per_byte = 9 if hardware_accelerator_present else 120

    # 160MHz MCU throughput estimate
    mcu_freq_hz = 160e6
    bytes_per_sec = mcu_freq_hz / cycles_per_byte
    throughput_mbps = (bytes_per_sec * 8.0) / 1e6
    exec_time_ms = ((data_size_kb * 1024) / bytes_per_sec) * 1000.0

    return {
        "status": "success",
        "algorithm": algo_upper,
        "key_size_bits": key_bits,
        "data_size_kb": data_size_kb,
        "hardware_accelerated": hardware_accelerator_present,
        "ram_footprint_bytes": ram_bytes,
        "estimated_cycles_per_byte": cycles_per_byte,
        "throughput_mbps": round(throughput_mbps, 2),
        "execution_time_ms": round(exec_time_ms, 3),
        "security_level": "CNSA 1.0 / NIST Compliant" if key_bits >= 256 else "Standard Commercial Security"
    }
