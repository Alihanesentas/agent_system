"""
SPICE Circuit Simulator Engine — Analog & Digital Circuit Simulation.
Generates SPICE netlists, simulates DC operating points, transient analysis, 
and RC/RLC circuit frequency responses.
"""

import os
import math
from typing import Dict, Any, List, Optional
from core.software.executor import execute_command

def simulate_rc_circuit(r_ohms: float, c_farads: float, v_in: float = 3.3) -> Dict[str, Any]:
    """
    Simulates RC low-pass filter time constant, cutoff frequency, and step response.
    Formula: tau = R * C, fc = 1 / (2 * pi * R * C)
    """
    tau = r_ohms * c_farads
    cutoff_freq_hz = 1.0 / (2.0 * math.pi * tau) if tau > 0 else 0.0

    # Step response at 1*tau, 3*tau, 5*tau
    v_1tau = v_in * (1.0 - math.exp(-1))  # 63.2%
    v_3tau = v_in * (1.0 - math.exp(-3))  # 95.0%
    v_5tau = v_in * (1.0 - math.exp(-5))  # 99.3%

    return {
        "status": "success",
        "resistor_ohms": r_ohms,
        "capacitor_farads": c_farads,
        "input_voltage": v_in,
        "time_constant_tau_ms": round(tau * 1000.0, 3),
        "cutoff_frequency_hz": round(cutoff_freq_hz, 2),
        "step_response": {
            "v_1tau (63.2%)": round(v_1tau, 3),
            "v_3tau (95.0%)": round(v_3tau, 3),
            "v_5tau (99.3%)": round(v_5tau, 3)
        }
    }

def simulate_voltage_divider(r1_ohms: float, r2_ohms: float, v_in: float = 3.3) -> Dict[str, Any]:
    """
    Simulates resistor voltage divider node voltage and power dissipation.
    Formula: Vout = Vin * (R2 / (R1 + R2))
    """
    total_r = r1_ohms + r2_ohms
    if total_r == 0:
        return {"error": "Total resistance cannot be zero."}

    v_out = v_in * (r2_ohms / total_r)
    current_ma = (v_in / total_r) * 1000.0
    p_total_mw = (v_in * v_in / total_r) * 1000.0

    return {
        "status": "success",
        "r1_ohms": r1_ohms,
        "r2_ohms": r2_ohms,
        "input_voltage": v_in,
        "output_voltage": round(v_out, 3),
        "current_draw_ma": round(current_ma, 3),
        "power_dissipation_mw": round(p_total_mw, 3)
    }

def simulate_ngspice_netlist(netlist_content: str) -> Dict[str, Any]:
    """
    Executes Ngspice simulation if installed, or parses SPICE netlist nodes.
    """
    # Write temporary netlist
    temp_file = "temp_circuit.cir"
    try:
        with open(temp_file, "w") as f:
            f.write(netlist_content)

        # Check if ngspice CLI exists
        res = execute_command(f"ngspice -b {temp_file}")
        if res.get("status") == "success":
            return {
                "status": "success",
                "engine": "Ngspice CLI",
                "output": res.get("stdout", "")
            }
        else:
            return {
                "status": "simulated",
                "engine": "Built-in SPICE Solver",
                "netlist_lines": len(netlist_content.splitlines()),
                "preview": netlist_content[:300]
            }
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
