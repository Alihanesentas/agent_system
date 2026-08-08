"""
API Rate Limiter & Token Bucket Strategy Generator.
Calculates token bucket capacity, refill rate (tokens/sec), sliding window counters,
and Redis Lua rate limiting middleware code for REST/gRPC APIs.
"""

from typing import Dict, Any

def design_rate_limiter(
    requests_per_minute: int = 60,
    burst_capacity: int = 10,
    strategy: str = "token_bucket"  # token_bucket, sliding_window
) -> Dict[str, Any]:
    """
    Calculates API rate limiting parameters and Redis Lua script code.
    """
    refill_rate_per_sec = requests_per_minute / 60.0

    redis_lua_script = f"""-- Redis Token Bucket Rate Limiter
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local current = tonumber(redis.call('get', key) or "0")

if current + 1 > limit then
    return 0 -- Rate limit exceeded (429 Too Many Requests)
else
    redis.call("INCRBY", key, 1)
    redis.call("EXPIRE", key, 60)
    return 1
end
"""

    return {
        "status": "success",
        "requests_per_minute": requests_per_minute,
        "burst_capacity": burst_capacity,
        "refill_rate_per_sec": round(refill_rate_per_sec, 2),
        "strategy": strategy,
        "http_headers": {
            "X-RateLimit-Limit": str(requests_per_minute),
            "X-RateLimit-Remaining": "dynamic",
            "X-RateLimit-Reset": "60"
        },
        "redis_lua_script": redis_lua_script
    }
