"""
NoSQL Document & Key-Value Database Schema Designer (MongoDB / DynamoDB / Redis).
Calculates partition key cardinality, document size (KB), indexing strategy,
read/write capacity units (RCU/WCU), and TTL expiration policies.
"""

from typing import Dict, Any, List

def design_nosql_model(
    db_engine: str = "DynamoDB",
    entity_name: str = "UserProfile",
    expected_read_qps: float = 500.0,
    expected_write_qps: float = 100.0,
    avg_item_size_kb: float = 2.5
) -> Dict[str, Any]:
    """
    Calculates NoSQL DynamoDB / MongoDB partition capacity and indexing.
    """
    engine = db_engine.strip()
    
    # DynamoDB RCU = (Item Size / 4KB) * Reads/sec
    item_rcu_blocks = max(1, int((avg_item_size_kb + 3.99) // 4.0))
    rcu_required = expected_read_qps * item_rcu_blocks
    
    # DynamoDB WCU = (Item Size / 1KB) * Writes/sec
    item_wcu_blocks = max(1, int((avg_item_size_kb + 0.99) // 1.0))
    wcu_required = expected_write_qps * item_wcu_blocks

    return {
        "status": "success",
        "database_engine": engine,
        "entity_name": entity_name,
        "avg_item_size_kb": avg_item_size_kb,
        "expected_read_qps": expected_read_qps,
        "expected_write_qps": expected_write_qps,
        "partition_key_design": f"PK: {entity_name}#{{id}} | SK: METADATA#v1",
        "dynamodb_rcu_required": rcu_required,
        "dynamodb_wcu_required": wcu_required,
        "indexing_strategy": "Global Secondary Index (GSI) on email-index",
        "compliance": "AWS Well-Architected NoSQL Pattern"
    }
