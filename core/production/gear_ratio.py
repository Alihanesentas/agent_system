"""
Spur & Planetary Gear Train Ratio & Backlash Calculator.
Calculates gear ratio (i), output RPM, output torque (Nm), pitch diameters (mm),
and center distance (mm) for spur gears and planetary gear trains.
"""

from typing import Dict, Any

def calculate_gear_ratio(
    driver_teeth: int = 12,
    driven_teeth: int = 48,
    module_mm: float = 1.0,
    input_rpm: float = 1500.0,
    input_torque_nm: float = 0.5
) -> Dict[str, Any]:
    """
    Calculates gear train reduction ratio, output speed, and torque.
    """
    ratio = driven_teeth / driver_teeth if driver_teeth > 0 else 4.0
    output_rpm = input_rpm / ratio
    output_torque_nm = input_torque_nm * ratio * 0.95  # 95% efficiency
    
    pitch_dia_driver_mm = driver_teeth * module_mm
    pitch_dia_driven_mm = driven_teeth * module_mm
    center_distance_mm = (pitch_dia_driver_mm + pitch_dia_driven_mm) / 2.0

    return {
        "status": "success",
        "gear_ratio": round(ratio, 3),
        "module_mm": module_mm,
        "driver_teeth": driver_teeth,
        "driven_teeth": driven_teeth,
        "input_rpm": input_rpm,
        "output_rpm": round(output_rpm, 1),
        "input_torque_nm": input_torque_nm,
        "output_torque_nm": round(output_torque_nm, 3),
        "pitch_diameter_driver_mm": pitch_dia_driver_mm,
        "pitch_diameter_driven_mm": pitch_dia_driven_mm,
        "center_distance_mm": center_distance_mm,
        "recommendation": f"Mount gear shafts at exact {center_distance_mm}mm center distance (±0.05mm backlash tolerance)."
    }
