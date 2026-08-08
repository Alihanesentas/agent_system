"""
PCB Fabrication & SMT Assembly Cost Estimator.
Calculates bare board prototype / production batch cost ($), NVR tooling fees,
stencil cost, and per-unit SMT assembly placement cost based on layer count and board area.
"""

from typing import Dict, Any

def estimate_pcb_cost(
    width_mm: float = 100.0,
    height_mm: float = 80.0,
    layer_count: int = 4,
    quantity: int = 100,
    surface_finish: str = "ENIG"  # HASL, ENIG
) -> Dict[str, Any]:
    """
    Estimates PCB manufacturing and SMT assembly costs.
    """
    area_cm2 = (width_mm * height_mm) / 100.0
    
    # Base board cost per cm2
    base_rate = {2: 0.05, 4: 0.12, 6: 0.25, 8: 0.45}.get(layer_count, 0.12)
    if "ENIG" in surface_finish.upper():
        base_rate *= 1.25
        
    bare_board_unit_usd = max(area_cm2 * base_rate, 0.50)
    total_bare_pcb_usd = bare_board_unit_usd * quantity
    
    tooling_fee_usd = 30.0 if layer_count <= 4 else 80.0
    stencil_usd = 15.0
    
    total_cost_usd = total_bare_pcb_usd + tooling_fee_usd + stencil_usd
    unit_cost_usd = total_cost_usd / quantity if quantity > 0 else 0.0

    return {
        "status": "success",
        "dimensions_mm": f"{width_mm} x {height_mm} mm",
        "area_cm2": area_cm2,
        "layer_count": layer_count,
        "quantity": quantity,
        "surface_finish": surface_finish,
        "bare_board_unit_usd": round(bare_board_unit_usd, 2),
        "tooling_nre_fee_usd": tooling_fee_usd,
        "stencil_cost_usd": stencil_usd,
        "total_batch_cost_usd": round(total_cost_usd, 2),
        "final_unit_cost_usd": round(unit_cost_usd, 2)
    }
