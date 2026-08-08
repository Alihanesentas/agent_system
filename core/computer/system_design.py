r"""
Distributed System Architecture Back-of-The-Envelope Capacity Estimator.
Calculates Daily Active Users (DAU), Queries Per Second (QPS), peak QPS ($2\times QPS$),
storage bandwidth ($TB/year$), RAM cache capacity ($20\%$ hot data rule), and server instance counts.
"""

from typing import Dict, Any

def estimate_system_design(
    daily_active_users: int = 10000000,  # 10M DAU
    actions_per_user_day: int = 20,
    payload_size_kb: float = 2.0
) -> Dict[str, Any]:
    """
    Calculates system QPS, storage bandwidth, and cache requirements.
    """
    total_daily_requests = daily_active_users * actions_per_user_day
    
    # Average QPS = Daily Requests / 86400 seconds
    avg_qps = total_daily_requests / 86400.0
    peak_qps = avg_qps * 2.0
    
    # Daily storage in GB = (Daily Requests * Payload KB) / (1024 * 1024)
    daily_storage_gb = (total_daily_requests * payload_size_kb) / (1024.0 * 1024.0)
    yearly_storage_tb = (daily_storage_gb * 365.0) / 1024.0
    
    # 20/80 Pareto Cache Rule: Cache 20% of daily data volume in RAM (Redis)
    recommended_cache_ram_gb = (daily_storage_gb * 0.20)

    return {
        "status": "success",
        "daily_active_users_dau": daily_active_users,
        "total_daily_requests": total_daily_requests,
        "average_qps": round(avg_qps, 1),
        "peak_qps": round(peak_qps, 1),
        "daily_storage_gb": round(daily_storage_gb, 2),
        "yearly_storage_tb": round(yearly_storage_tb, 2),
        "redis_cache_ram_required_gb": round(recommended_cache_ram_gb, 2),
        "recommended_app_servers": max(2, int(peak_qps // 500.0))  # ~500 QPS per instance
    }
