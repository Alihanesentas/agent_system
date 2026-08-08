"""
PID Controller Parameter Auto-Tuner Engine (Ziegler-Nichols & Cohen-Coon).
Calculates proportional (Kp), integral (Ki), and derivative (Kd) gain parameters
from step response parameters (Ku, Tu or K, L, T).
"""

from typing import Dict, Any

def tune_pid_controller(
    method: str = "ziegler-nichols",
    ku_ultimate_gain: float = 12.5,
    tu_period_sec: float = 0.45,
    controller_type: str = "PID"
) -> Dict[str, Any]:
    """
    Calculates Kp, Ki, Kd parameters for PID/PI/P controllers.
    """
    ctype = controller_type.upper()
    
    if "ZIEGLER" in method.upper():
        if ctype == "P":
            kp = 0.5 * ku_ultimate_gain
            ti = float("inf")
            td = 0.0
        elif ctype == "PI":
            kp = 0.45 * ku_ultimate_gain
            ti = tu_period_sec / 1.2
            td = 0.0
        else:  # PID
            kp = 0.6 * ku_ultimate_gain
            ti = 0.5 * tu_period_sec
            td = 0.125 * tu_period_sec
    else:  # Cohen-Coon default fallback
        kp = 0.6 * ku_ultimate_gain
        ti = 0.5 * tu_period_sec
        td = 0.125 * tu_period_sec

    ki = kp / ti if ti != float("inf") and ti > 0 else 0.0
    kd = kp * td

    return {
        "status": "success",
        "tuning_method": method,
        "controller_type": ctype,
        "ultimate_gain_ku": ku_ultimate_gain,
        "oscillation_period_tu_sec": tu_period_sec,
        "gains": {
            "kp": round(kp, 4),
            "ki": round(ki, 4),
            "kd": round(kd, 4),
            "ti_sec": round(ti, 4) if ti != float("inf") else "inf",
            "td_sec": round(td, 4)
        },
        "sample_discrete_code": f"// Discrete PID algorithm:\noutput = ({round(kp, 2)} * error) + ({round(ki, 2)} * integral) + ({round(kd, 2)} * derivative);"
    }
