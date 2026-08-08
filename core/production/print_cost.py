"""
3D Printing Cost & Material Cost Estimator Engine.
Calculates total 3D printing manufacturing cost based on filament weight (g),
print time (hours), material type (PLA/PETG/ABS/TPU), power consumption (kWh), and printer depreciation.
"""

from typing import Dict, Any

MATERIAL_PRICES_PER_KG = {
    "PLA": 22.0,
    "PETG": 25.0,
    "ABS": 28.0,
    "TPU": 35.0,
    "NYLON": 55.0,
    "PC": 65.0
}

def estimate_3d_print_cost(
    weight_g: float = 85.0,
    print_time_hours: float = 4.5,
    material: str = "PETG",
    kwh_cost_usd: float = 0.15,
    printer_power_w: float = 200.0,
    labor_hourly_rate_usd: float = 15.0
) -> Dict[str, Any]:
    """
    Estimates total 3D print manufacturing cost breakdown.
    """
    mat_upper = material.upper()
    mat_price_kg = MATERIAL_PRICES_PER_KG.get(mat_upper, 25.0)
    
    mat_cost = (weight_g / 1000.0) * mat_price_kg
    power_kwh = (printer_power_w / 1000.0) * print_time_hours
    power_cost = power_kwh * kwh_cost_usd
    machine_depreciation = print_time_hours * 0.50  # $0.50/hr wear
    labor_cost = 0.1 * labor_hourly_rate_usd  # 6 mins setup/post processing
    
    total_cost = mat_cost + power_cost + machine_depreciation + labor_cost

    return {
        "status": "success",
        "material": mat_upper,
        "weight_g": weight_g,
        "print_time_hours": print_time_hours,
        "cost_breakdown_usd": {
            "material_cost": round(mat_cost, 2),
            "electricity_cost": round(power_cost, 2),
            "machine_wear_cost": round(machine_depreciation, 2),
            "labor_post_processing": round(labor_cost, 2)
        },
        "total_unit_cost_usd": round(total_cost, 2),
        "recommended_retail_price_usd": round(total_cost * 2.5, 2)
    }
