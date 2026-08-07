"""
BOM Component Cost Sensitivity & Inflation Risk Analyzer.
Performs Monte Carlo sensitivity analysis on BOM component price swings under inflation
or component shortages.
"""

import random
from typing import Dict, Any, List

def analyze_bom_cost_sensitivity(
    base_unit_cost_usd: float = 6.45,
    inflation_margin_pct: float = 15.0
) -> Dict[str, Any]:
    """Runs Monte Carlo simulations on BOM price swings under supply chain shock."""
    simulations = []
    for i in range(10):
        swing = random.uniform(-inflation_margin_pct, inflation_margin_pct)
        sim_cost = base_unit_cost_usd * (1.0 + (swing / 100.0))
        simulations.append(round(sim_cost, 2))

    max_cost = max(simulations)
    min_cost = min(simulations)
    avg_cost = round(sum(simulations) / len(simulations), 2)

    return {
        "status": "success",
        "base_unit_cost_usd": base_unit_cost_usd,
        "simulated_min_cost_usd": min_cost,
        "simulated_max_cost_usd": max_cost,
        "simulated_avg_cost_usd": avg_cost,
        "cost_variance_range_usd": round(max_cost - min_cost, 2)
    }
