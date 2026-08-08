"""
PCB Array Panelization & Breakaway Tab Optimizer.
Calculates panel grid layout (X x Y), total boards per panel, panel utilization efficiency (%),
breakaway V-score vs Mouse-bite tab specs, and tooling rail width (mm).
"""

from typing import Dict, Any

def optimize_pcb_panel(
    board_length_mm: float = 50.0,
    board_width_mm: float = 30.0,
    panel_max_length_mm: float = 300.0,
    panel_max_width_mm: float = 200.0,
    tooling_rail_width_mm: float = 10.0,
    board_spacing_mm: float = 2.0
) -> Dict[str, Any]:
    """
    Optimizes PCB array panelization and calculates material utilization efficiency.
    """
    usable_length = panel_max_length_mm - (2 * tooling_rail_width_mm)
    usable_width = panel_max_width_mm - (2 * tooling_rail_width_mm)
    
    count_x = int((usable_length + board_spacing_mm) // (board_length_mm + board_spacing_mm))
    count_y = int((usable_width + board_spacing_mm) // (board_width_mm + board_spacing_mm))
    
    total_boards = count_x * count_y
    
    board_area = board_length_mm * board_width_mm * total_boards
    panel_area = panel_max_length_mm * panel_max_width_mm
    efficiency_pct = (board_area / panel_area) * 100.0 if panel_area > 0 else 0.0

    return {
        "status": "success",
        "single_board_mm": f"{board_length_mm} x {board_width_mm}",
        "max_panel_mm": f"{panel_max_length_mm} x {panel_max_width_mm}",
        "grid_layout": f"{count_x} x {count_y}",
        "total_boards_per_panel": total_boards,
        "panel_utilization_efficiency_pct": round(efficiency_pct, 2),
        "tooling_rail_width_mm": tooling_rail_width_mm,
        "recommended_depanelization": "V-Scoring (1/3 Web)" if board_spacing_mm <= 0 else "Mouse-Bites (5-hole 0.8mm array)"
    }
