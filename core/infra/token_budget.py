"""
Token Cost Budgeting & Dollar Alert Engine.
Tracks daily/monthly token spending ($), alerting when approaching 80% or 100% of user budget caps.
"""

from typing import Dict, Any

class TokenBudgetTracker:
    def __init__(self, monthly_cap_usd: float = 50.0):
        self.monthly_cap_usd = monthly_cap_usd
        self.current_spent_usd = 0.0

    def add_cost(self, cost_usd: float) -> Dict[str, Any]:
        """Tracks token expenditure and alerts if budget exceeded."""
        self.current_spent_usd += cost_usd
        used_pct = round((self.current_spent_usd / self.monthly_cap_usd) * 100.0, 1)
        
        status = "OK"
        if used_pct >= 100.0:
            status = "BUDGET_EXCEEDED"
        elif used_pct >= 80.0:
            status = "BUDGET_WARNING_80_PCT"

        return {
            "status": status,
            "current_spent_usd": round(self.current_spent_usd, 4),
            "monthly_cap_usd": self.monthly_cap_usd,
            "budget_used_pct": used_pct
        }

global_token_budget = TokenBudgetTracker(monthly_cap_usd=50.0)
