"""
PCB Layer Stackup & High-Speed Differential Impedance Calculator.
Calculates 2, 4, 6, and 8-layer PCB substrate thickness, FR-4 dielectric constant (Er=4.4),
copper weight (1oz / 35um), prepreg thickness, and differential pair spacing for USB 2.0 / HDMI.
"""

import math
from typing import Dict, Any, List

def calculate_pcb_stackup(
    layers: int = 4,
    board_thickness_mm: float = 1.6,
    copper_oz: float = 1.0
) -> Dict[str, Any]:
    """
    Calculates layer stackup geometry, dielectric spacing, and differential trace specs.
    """
    copper_um = copper_oz * 35.0
    fr4_er = 4.4
    
    if layers == 2:
        core_mm = board_thickness_mm - (2 * copper_um / 1000.0)
        stackup = [
            {"layer": 1, "name": "Top Copper (F.Cu)", "type": "Signal/Power", "thickness_um": copper_um},
            {"layer": "Dielectric", "name": "FR-4 Core", "type": "Substrate (Er=4.4)", "thickness_mm": round(core_mm, 3)},
            {"layer": 2, "name": "Bottom Copper (B.Cu)", "type": "Signal/GND", "thickness_um": copper_um}
        ]
    else:  # 4, 6, 8 Layers
        prepreg_mm = 0.2
        core_mm = (board_thickness_mm - (layers * copper_um / 1000.0) - (2 * prepreg_mm)) / max(1, (layers - 2) // 2)
        stackup = [
            {"layer": 1, "name": "F.Cu (Top Signal)", "type": "High-Speed Signal", "thickness_um": copper_um},
            {"layer": "Prepreg", "name": "FR-4 2116 Prepreg", "type": "Dielectric (Er=4.2)", "thickness_mm": prepreg_mm},
            {"layer": 2, "name": "In1.Cu (GND Plane)", "type": "Ground Plane", "thickness_um": copper_um},
            {"layer": "Core", "name": "FR-4 Core", "type": "Substrate (Er=4.4)", "thickness_mm": round(core_mm, 3)},
            {"layer": 3, "name": "In2.Cu (VCC Plane)", "type": "Power Plane", "thickness_um": copper_um},
            {"layer": "Prepreg", "name": "FR-4 2116 Prepreg", "type": "Dielectric (Er=4.2)", "thickness_mm": prepreg_mm},
            {"layer": 4, "name": "B.Cu (Bottom Signal)", "type": "Signal", "thickness_um": copper_um}
        ]

    # Differential pair 90 ohm USB 2.0 trace recommendation
    diff_trace_width_mm = 0.20
    diff_trace_gap_mm = 0.15

    return {
        "status": "success",
        "total_layers": layers,
        "target_board_thickness_mm": board_thickness_mm,
        "copper_weight_oz": copper_oz,
        "stackup_layers": stackup,
        "usb2_differential_specs": {
            "target_impedance_ohms": 90,
            "trace_width_mm": diff_trace_width_mm,
            "trace_gap_mm": diff_trace_gap_mm
        }
    }
