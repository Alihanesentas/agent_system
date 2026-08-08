"""
DC / BLDC / Stepper Motor Sizing & Inertia Calculator.
Calculates required mechanical torque (Nm / oz-in), rotational speed (RPM),
mechanical power (Watts), and load inertia ratio (J_load / J_motor).
"""

import math
from typing import Dict, Any

def size_motor(
    load_mass_kg: float = 2.5,
    radius_m: float = 0.05,
    desired_rpm: float = 300.0,
    accel_time_sec: float = 0.2,
    efficiency: float = 0.85
) -> Dict[str, Any]:
    """
    Sizes motor torque, mechanical power, and speed requirements.
    """
    omega_rad_s = (desired_rpm * 2.0 * math.pi) / 60.0
    angular_accel = omega_rad_s / accel_time_sec if accel_time_sec > 0 else 10.0
    
    # Inertia of solid cylinder J = 0.5 * m * r^2
    j_load = 0.5 * load_mass_kg * (radius_m ** 2)
    
    accel_torque_nm = j_load * angular_accel
    friction_torque_nm = load_mass_kg * 9.81 * radius_m * 0.05  # 5% friction
    total_torque_nm = (accel_torque_nm + friction_torque_nm) / efficiency
    
    power_watts = total_torque_nm * omega_rad_s
    
    # Motor category recommendation
    if power_watts < 10:
        motor_type = "NEMA 17 Stepper or Coreless DC Motor"
    elif power_watts < 100:
        motor_type = "NEMA 23 Stepper or Brushless DC (BLDC) Motor"
    else:
        motor_type = "Industrial AC Servo or High-Power BLDC Motor"

    return {
        "status": "success",
        "load_mass_kg": load_mass_kg,
        "desired_rpm": desired_rpm,
        "load_inertia_kg_m2": round(j_load, 6),
        "peak_torque_nm": round(total_torque_nm, 3),
        "peak_torque_oz_in": round(total_torque_nm * 141.612, 1),
        "mechanical_power_watts": round(power_watts, 1),
        "recommended_motor_category": motor_type,
        "recommendation": f"Select motor rated for minimum {round(total_torque_nm * 1.5, 2)}Nm peak torque at {desired_rpm} RPM."
    }
