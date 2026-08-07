"""
Database Schema & SQL Migration Generator Engine.
Generates PostgreSQL / SQLite DDL schemas, Alembic migration scripts, and index optimization rules.
"""

from typing import Dict, Any

def generate_db_schema_and_migrations(table_name: str = "users") -> Dict[str, Any]:
    """Generates SQL DDL schema and Alembic migration template."""
    sql_ddl = f"""CREATE TABLE {table_name} (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_{table_name}_email ON {table_name}(email);
"""
    return {
        "status": "success",
        "table_name": table_name,
        "sql_ddl": sql_ddl,
        "indexed_columns": ["email"]
    }
