"""
Pinout Conflict Checker — Hardware Pin Assignment & Collision Analysis.
Detects GPIO pin collisions (I2C SDA/SCL, SPI MOSI/MISO/SCK/CS, UART TX/RX, ADC) 
for ESP32, STM32, and RP2040 microcontrollers.
"""

from typing import Dict, Any, List, Optional

MCU_PIN_CAPABILITIES: Dict[str, Dict[str, List[str]]] = {
    "ESP32": {
        "strapping_pins": ["GPIO0", "GPIO2", "GPIO5", "GPIO12", "GPIO15"],
        "input_only_pins": ["GPIO34", "GPIO35", "GPIO36", "GPIO39"],
        "recommended_i2c": ["GPIO21", "GPIO22"],
        "recommended_spi": ["GPIO18", "GPIO19", "GPIO23", "GPIO5"],
        "recommended_uart": ["GPIO1", "GPIO3"]
    },
    "STM32F103": {
        "i2c1": ["PB6", "PB7"],
        "spi1": ["PA5", "PA6", "PA7", "PA4"],
        "usart1": ["PA9", "PA10"],
        "adc_pins": ["PA0", "PA1", "PA2", "PA3", "PA4", "PA5", "PA6", "PA7"]
    },
    "RP2040": {
        "i2c0": ["GPIO4", "GPIO5"],
        "spi0": ["GPIO16", "GPIO17", "GPIO18", "GPIO19"],
        "uart0": ["GPIO0", "GPIO1"]
    }
}

def check_pinout_conflicts(pin_assignments: Dict[str, str], mcu_family: str = "ESP32") -> Dict[str, Any]:
    """
    Checks pin assignment dictionary for hardware conflicts, strapping pin hazards, 
    and input-only pin violations.
    
    Example pin_assignments:
        {"I2C_SDA": "GPIO21", "I2C_SCL": "GPIO22", "BUTTON": "GPIO34", "LED": "GPIO34"}
    """
    conflicts: List[str] = []
    warnings: List[str] = []
    seen_pins: Dict[str, str] = {}

    mcu_info = MCU_PIN_CAPABILITIES.get(mcu_family.upper(), MCU_PIN_CAPABILITIES["ESP32"])

    for net_name, pin in pin_assignments.items():
        pin_upper = pin.upper().strip()

        # 1. Collision check (same pin assigned to multiple nets)
        if pin_upper in seen_pins:
            conflicts.append(f"🔴 PIN COLLISION: Pin '{pin_upper}' is assigned to both '{seen_pins[pin_upper]}' and '{net_name}'!")
        else:
            seen_pins[pin_upper] = net_name

        # 2. ESP32 Input-Only pins check (GPIO34-39 cannot be outputs)
        if mcu_family.upper() == "ESP32":
            if pin_upper in mcu_info.get("input_only_pins", []):
                if any(out_kw in net_name.upper() for out_kw in ["LED", "TX", "MOSI", "SCK", "PWM", "RELAY", "BUZZER"]):
                    conflicts.append(f"🔴 OUTPUT VIOLATION: Pin '{pin_upper}' assigned to '{net_name}' is INPUT-ONLY on ESP32!")

            # 3. Strapping pin warning
            if pin_upper in mcu_info.get("strapping_pins", []):
                warnings.append(f"⚠️ STRAPPING PIN HAZARD: '{pin_upper}' ({net_name}) is a boot strapping pin. Pull resistor must not affect boot mode!")

    return {
        "status": "conflict_detected" if conflicts else "clean",
        "mcu_family": mcu_family,
        "total_pins_assigned": len(pin_assignments),
        "conflicts": conflicts,
        "warnings": warnings,
        "pin_map": seen_pins
    }
