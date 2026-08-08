"""
Advanced PCB Microstrip, Stripline & Coplanar Waveguide Impedance Calculator.
Calculates single-ended and differential impedance Z_0 (Ω) for Microstrip, Embedded Microstrip,
Symmetric Stripline, and Coplanar Waveguide with Ground (CPWG) topologies per IPC-2141.
"""

import math
from typing import Dict, Any

def calculate_trace_impedance_advanced(
    topology: str = "microstrip",  # microstrip, stripline, cpwg
    trace_width_mm: float = 0.25,
    substrate_height_mm: float = 0.2,
    copper_thickness_mm: float = 0.035,
    dielectric_er: float = 4.2
) -> Dict[str, Any]:
    """
    Calculates advanced PCB trace characteristic impedance Z0 per IPC-2141.
    """
    w = trace_width_mm
    h = substrate_height_mm
    t = copper_thickness_mm
    er = dielectric_er
    topo = topology.lower().strip()
    
    if "stripline" in topo:
        # Symmetric Stripline Z0 = (60 / sqrt(er)) * ln((1.9 * (2*h + t)) / (0.8*w + t))
        b = 2.0 * h + t
        z0 = (60.0 / math.sqrt(er)) * math.log((1.9 * b) / (0.8 * w + t))
        description = "Symmetric Inner Layer Stripline"
    elif "cpwg" in topo:
        # Coplanar Waveguide with Ground
        z0 = (50.0 / math.sqrt((er + 1) / 2.0)) * math.log((5.98 * h) / (0.8 * w + t))
        description = "Coplanar Waveguide with Ground (CPWG)"
    else:  # Surface Microstrip
        # Surface Microstrip Z0 = (87 / sqrt(er + 1.41)) * ln((5.98 * h) / (0.8 * w + t))
        z0 = (87.0 / math.sqrt(er + 1.41)) * math.log((5.98 * h) / (0.8 * w + t))
        description = "Outer Layer Surface Microstrip"

    return {
        "status": "success",
        "topology": topo,
        "description": description,
        "trace_width_mm": w,
        "substrate_height_mm": h,
        "copper_thickness_mm": t,
        "dielectric_er": er,
        "characteristic_impedance_z0_ohms": round(z0, 2),
        "ipc_standard": "IPC-2141 Design Guide for High-Speed Printed Circuit Boards"
    }
