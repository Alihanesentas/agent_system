"""
Battery Life & Solar Power Calculator Module.
Calculates battery operational lifespan (LiPo / 18650 / CR2032) for IoT devices
based on active and deep-sleep duty cycles, and calculates solar panel wattage requirements.
"""

from typing import Dict, Any

def calculate_battery_lifespan(
    battery_capacity_mah: float = 2500.0,  # 18650 Cell
    active_current_ma: float = 80.0,       # ESP32 active TX
    active_time_sec_per_min: float = 2.0,  # 2 seconds per minute active
    sleep_current_ua: float = 15.0         # Deep sleep micro-amps
) -> Dict[str, Any]:
    """
    Calculates average current consumption and battery lifespan in days/months.
    """
    active_duty = active_time_sec_per_min / 60.0
    sleep_duty = 1.0 - active_duty

    active_current_avg_ma = active_current_ma * active_duty
    sleep_current_avg_ma = (sleep_current_ua / 1000.0) * sleep_duty

    total_avg_current_ma = active_current_avg_ma + sleep_current_avg_ma

    # 85% usable battery capacity factor
    usable_capacity_mah = battery_capacity_mah * 0.85
    lifespan_hours = usable_capacity_mah / total_avg_current_ma
    lifespan_days = round(lifespan_hours / 24.0, 1)
    lifespan_months = round(lifespan_days / 30.0, 1)

    # Solar sizing: Wattage needed to recharge daily usage in 4 hours peak sun
    daily_mah = total_avg_current_ma * 24.0
    daily_wh = (daily_mah / 1000.0) * 3.7
    solar_watts_needed = round((daily_wh / 4.0) * 1.5, 2)  # 1.5x efficiency margin

    return {
        "status": "success",
        "battery_capacity_mah": battery_capacity_mah,
        "average_current_draw_ma": round(total_avg_current_ma, 3),
        "estimated_lifespan_days": lifespan_days,
        "estimated_lifespan_months": lifespan_months,
        "recommended_solar_panel_watts": max(0.5, solar_watts_needed)
    }
