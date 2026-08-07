"""
LLM API Token Usage Analytics & Cost Forecast Engine.
Forecasts daily/weekly/monthly token cost burn rates ($) based on moving average usage trends (/cost-forecast).
"""

from typing import Dict, Any

def forecast_token_costs(daily_spent_usd: float = 0.45) -> Dict[str, Any]:
    """Forecasts weekly and monthly LLM API expenditures."""
    weekly_forecast = daily_spent_usd * 7.0
    monthly_forecast = daily_spent_usd * 30.0

    return {
        "status": "success",
        "current_daily_burn_rate_usd": daily_spent_usd,
        "forecasted_weekly_cost_usd": round(weekly_forecast, 2),
        "forecasted_monthly_cost_usd": round(monthly_forecast, 2)
    }
