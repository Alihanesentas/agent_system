"""
UART Baud Rate, Clock Divider & Error Percentage Calculator.
Calculates baud rate fractional clock dividers, baud rate error percentage (%),
and recommended peripheral clock settings for MCU UART controllers (STM32/ESP32/AVR).
"""

from typing import Dict, Any

def configure_uart(
    target_baud: int = 115200,
    mcu_clock_mhz: float = 80.0,
    oversampling: int = 16
) -> Dict[str, Any]:
    """
    Calculates UART integer and fractional clock dividers and error %.
    """
    clock_hz = mcu_clock_mhz * 1e6
    usart_div = clock_hz / (oversampling * target_baud)
    
    div_mantissa = int(usart_div)
    div_fraction = round((usart_div - div_mantissa) * oversampling)
    
    actual_div = div_mantissa + (div_fraction / float(oversampling))
    actual_baud = clock_hz / (oversampling * actual_div) if actual_div > 0 else target_baud
    
    error_pct = abs((actual_baud - target_baud) / target_baud) * 100.0

    return {
        "status": "success",
        "target_baud": target_baud,
        "mcu_clock_mhz": mcu_clock_mhz,
        "oversampling": oversampling,
        "usart_div_raw": round(usart_div, 4),
        "div_mantissa": div_mantissa,
        "div_fraction": div_fraction,
        "actual_baud": round(actual_baud, 1),
        "error_pct": round(error_pct, 3),
        "compliance": "PASSED (Error < 2.0%)" if error_pct < 2.0 else "WARN: Baud error > 2%, risk of framed bit corruption"
    }
