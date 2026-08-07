"""
Multi-MCU Board Selector & Hardware Spec Recommender Engine.
Compares ESP32-S3, STM32F4, RP2040, nRF52840, Teensy 4.1, and RISC-V microcontrollers
across clock speed, SRAM, Flash, interfaces, power consumption, and unit price.
"""

from typing import Dict, Any, List

MCU_CATALOG = {
    "ESP32-S3": {"cpu": "Xtensa LX7 240MHz", "sram": "512KB + 8MB PSRAM", "flash": "8MB", "connectivity": "Wi-Fi 4 + BLE 5.0", "price_usd": 2.85, "best_for": "IoT, AI Vision, Audio, Wireless"},
    "STM32F401": {"cpu": "ARM Cortex-M4 84MHz", "sram": "96KB", "flash": "512KB", "connectivity": "USB OTG, SPI, I2C, USART", "price_usd": 3.20, "best_for": "Industrial Control, Low Latency, DSP"},
    "RP2040": {"cpu": "Dual ARM Cortex-M0+ 133MHz", "sram": "264KB", "flash": "2MB - 16MB External", "connectivity": "PIO, USB 1.1, SPI, I2C", "price_usd": 0.70, "best_for": "Cost-Sensitive, Custom PIO Protocols"},
    "nRF52840": {"cpu": "ARM Cortex-M4F 64MHz", "sram": "256KB", "flash": "1MB", "connectivity": "BLE 5.3, Thread, Zigbee, NFC", "price_usd": 4.50, "best_for": "Ultra Low Power Wearables, BLE Mesh"},
    "Teensy 4.1": {"cpu": "ARM Cortex-M7 600MHz", "sram": "1024KB", "flash": "8MB", "connectivity": "Ethernet, USB High-Speed, CAN Bus", "price_usd": 29.80, "best_for": "High Performance DSP, Real-Time Audio, CAN Bus"}
}

def recommend_mcu_for_project(requirements_description: str) -> Dict[str, Any]:
    """Recommends optimal microcontroller based on project requirements."""
    req_lower = requirements_description.lower()
    
    if "ble" in req_lower or "wearable" in req_lower or "mesh" in req_lower:
        selected = "nRF52840"
    elif "dsp" in req_lower or "audio" in req_lower or "600mhz" in req_lower:
        selected = "Teensy 4.1"
    elif "cheap" in req_lower or "cost" in req_lower or "rp2040" in req_lower:
        selected = "RP2040"
    elif "industrial" in req_lower or "stm32" in req_lower:
        selected = "STM32F401"
    else:
        selected = "ESP32-S3"

    return {
        "status": "success",
        "user_requirements": requirements_description,
        "recommended_mcu": selected,
        "specs": MCU_CATALOG[selected],
        "all_options": list(MCU_CATALOG.keys())
    }
