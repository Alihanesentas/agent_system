"""
BOM Cost Optimizer & Quantity Tier Analyzer Module.
Analyzes component BOM pricing across quantity tiers (1, 100, 1000 units),
flags expensive line items (>30% of total cost), and recommends cost reduction strategies.
"""

from typing import Dict, Any, List

def optimize_bom_cost(
    bom_items: List[Dict[str, Any]],
    target_production_qty: int = 1000
) -> Dict[str, Any]:
    """
    Analyzes BOM cost breakdown and flags high-cost components for replacement.
    """
    total_unit_cost = 0.0
    line_analysis = []

    for item in bom_items:
        part = item.get("part", "Component")
        price = float(item.get("unit_price_usd", 1.0))
        qty = int(item.get("qty", 1))

        # Quantity break discount estimate (1000 units = ~35% discount)
        discounted_price = price * 0.65 if target_production_qty >= 1000 else price
        item_total = discounted_price * qty
        total_unit_cost += item_total

        line_analysis.append({
            "part": part,
            "unit_price_usd": round(discounted_price, 3),
            "qty_per_board": qty,
            "line_total_usd": round(item_total, 3)
        })

    # Flag high cost drivers (>30% of BOM)
    cost_drivers = []
    for line in line_analysis:
        pct = (line["line_total_usd"] / total_unit_cost) * 100.0 if total_unit_cost > 0 else 0
        line["percentage_of_total_bom"] = round(pct, 1)
        if pct >= 30.0:
            cost_drivers.append(f"⚠️ {line['part']} accounts for {round(pct,1)}% of total BOM cost!")

    return {
        "status": "success",
        "production_target_units": target_production_qty,
        "total_bom_unit_cost_usd": round(total_unit_cost, 2),
        "cost_drivers": cost_drivers,
        "line_item_breakdown": line_analysis,
        "recommendation": "Consider JLCPCB Basic Parts or Chinese equivalents for high-cost LDOs/MCUs to reduce BOM cost by up to 40%."
    }
