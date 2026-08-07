"""
Persistent Long-Term Memory — Cross-Session Decision & Knowledge Store.
Remembers project decisions, component selections, pinout choices, 
and design rationale across agent sessions using SQLite.
"""

import os
import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "memory_store.db")

def _get_conn() -> sqlite3.Connection:
    """Returns a connection to the long-term memory database, creating tables if needed."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            context TEXT DEFAULT '',
            agent_name TEXT DEFAULT 'orchestrator',
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now')),
            UNIQUE(category, key)
        )
    """)
    conn.commit()
    return conn

def remember(category: str, key: str, value: str, context: str = "", agent_name: str = "orchestrator") -> Dict[str, Any]:
    """
    Stores or updates a long-term memory entry.
    Categories: 'decision', 'component', 'pinout', 'design', 'config', 'note'
    """
    conn = _get_conn()
    try:
        conn.execute("""
            INSERT INTO memories (category, key, value, context, agent_name, updated_at)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
            ON CONFLICT(category, key) DO UPDATE SET
                value = excluded.value,
                context = excluded.context,
                agent_name = excluded.agent_name,
                updated_at = datetime('now')
        """, (category, key, value, context, agent_name))
        conn.commit()
        return {"status": "stored", "category": category, "key": key}
    finally:
        conn.close()

def recall(category: Optional[str] = None, key: Optional[str] = None, search_text: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Retrieves memories by category, key, or full-text search.
    Returns all matching memories sorted by most recently updated.
    """
    conn = _get_conn()
    try:
        query = "SELECT id, category, key, value, context, agent_name, created_at, updated_at FROM memories"
        conditions = []
        params = []

        if category:
            conditions.append("category = ?")
            params.append(category)
        if key:
            conditions.append("key LIKE ?")
            params.append(f"%{key}%")
        if search_text:
            conditions.append("(value LIKE ? OR context LIKE ? OR key LIKE ?)")
            params.extend([f"%{search_text}%"] * 3)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY updated_at DESC"

        cursor = conn.execute(query, params)
        rows = cursor.fetchall()

        return [
            {
                "id": r[0], "category": r[1], "key": r[2], "value": r[3],
                "context": r[4], "agent_name": r[5], "created_at": r[6], "updated_at": r[7]
            }
            for r in rows
        ]
    finally:
        conn.close()

def forget(category: str, key: str) -> Dict[str, Any]:
    """Deletes a specific memory entry."""
    conn = _get_conn()
    try:
        cursor = conn.execute("DELETE FROM memories WHERE category = ? AND key = ?", (category, key))
        conn.commit()
        return {"status": "deleted", "rows_affected": cursor.rowcount}
    finally:
        conn.close()

def recall_for_prompt(agent_name: Optional[str] = None, max_entries: int = 10) -> str:
    """
    Builds a formatted context string from long-term memory
    to inject into LLM prompts for cross-session continuity.
    """
    memories = recall()
    if agent_name:
        memories = [m for m in memories if m["agent_name"] == agent_name or m["agent_name"] == "orchestrator"]

    memories = memories[:max_entries]
    if not memories:
        return ""

    lines = ["=== LONG-TERM PROJECT MEMORY ==="]
    for m in memories:
        lines.append(f"[{m['category'].upper()}] {m['key']}: {m['value']}")
        if m['context']:
            lines.append(f"  Context: {m['context']}")
    lines.append("=== END MEMORY ===\n")

    return "\n".join(lines)

def get_memory_stats() -> Dict[str, Any]:
    """Returns statistics about the long-term memory store."""
    conn = _get_conn()
    try:
        total = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
        categories = conn.execute("SELECT category, COUNT(*) FROM memories GROUP BY category").fetchall()
        return {
            "total_entries": total,
            "categories": {cat: count for cat, count in categories},
            "db_path": DB_PATH
        }
    finally:
        conn.close()
