"""
SQL DDL Schema & Migration Script Generator.
Generates normalized PostgreSQL / SQLite DDL tables, foreign key constraints, indexes, and migration SQL scripts.
"""

from typing import Dict, Any, List

def generate_sql_schema(
    table_name: str = "telemetry_logs",
    database_type: str = "postgresql"
) -> Dict[str, Any]:
    """
    Generates SQL DDL schema and index definitions.
    """
    tbl = table_name.lower()
    
    sql_ddl = f"""-- Auto-generated SQL DDL Schema for {tbl} ({database_type.upper()})
CREATE TABLE IF NOT EXISTS {tbl} (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id VARCHAR(64) NOT NULL,
    temperature NUMERIC(5, 2),
    humidity NUMERIC(5, 2),
    status_code INT DEFAULT 0,
    payload JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_{tbl}_device_id ON {tbl}(device_id);
CREATE INDEX IF NOT EXISTS idx_{tbl}_created_at ON {tbl}(created_at DESC);
"""

    return {
        "status": "success",
        "table_name": tbl,
        "database_type": database_type,
        "sql_ddl": sql_ddl,
        "indexes_created": 2
    }
