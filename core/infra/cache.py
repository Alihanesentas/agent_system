import os
import sqlite3
import hashlib
from difflib import SequenceMatcher
from datetime import datetime
from typing import Optional, Dict, Any, Tuple

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "subagent_tracker", "backend", "tracker.db")

def init_cache_table():
    """Initializes the semantic cache table in SQLite."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS semanticcache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt_hash TEXT UNIQUE,
            prompt_text TEXT,
            response_text TEXT,
            agent_name TEXT,
            model_name TEXT,
            hit_count INTEGER DEFAULT 0,
            tokens_saved INTEGER DEFAULT 0,
            cost_saved_usd REAL DEFAULT 0.0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def _compute_hash(text: str) -> str:
    """Computes SHA-256 hash of normalized text."""
    normalized = " ".join(text.lower().strip().split())
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()

def find_cached_response(
    prompt: str, 
    agent_name: str = "orchestrator", 
    similarity_threshold: float = 0.88
) -> Optional[Dict[str, Any]]:
    """
    Searches for an exact or semantically similar cached LLM response.
    Returns cached response dict if found, else None.
    """
    init_cache_table()
    prompt_hash = _compute_hash(prompt)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Exact hash lookup (Instant O(1) hit)
    cursor.execute("""
        SELECT id, response_text, model_name, hit_count, tokens_saved 
        FROM semanticcache 
        WHERE prompt_hash = ? AND agent_name = ?
    """, (prompt_hash, agent_name))
    row = cursor.fetchone()

    if row:
        cache_id, response, model_name, hit_count, tokens_saved = row
        # Update hit count
        cursor.execute("UPDATE semanticcache SET hit_count = hit_count + 1 WHERE id = ?", (cache_id,))
        conn.commit()
        conn.close()
        return {
            "cache_id": cache_id,
            "response": response,
            "model_name": model_name,
            "similarity": 1.0,
            "is_exact": True
        }

    # 2. Fuzzy semantic similarity lookup across recent cached prompts
    cursor.execute("SELECT id, prompt_text, response_text, model_name FROM semanticcache WHERE agent_name = ?", (agent_name,))
    cached_entries = cursor.fetchall()
    
    best_match = None
    best_score = 0.0

    normalized_prompt = " ".join(prompt.lower().strip().split())

    for c_id, c_prompt, c_response, c_model in cached_entries:
        norm_c_prompt = " ".join(c_prompt.lower().strip().split())
        score = SequenceMatcher(None, normalized_prompt, norm_c_prompt).ratio()
        if score > best_score:
            best_score = score
            best_match = (c_id, c_response, c_model)

    if best_match and best_score >= similarity_threshold:
        cache_id, response, model_name = best_match
        cursor.execute("UPDATE semanticcache SET hit_count = hit_count + 1 WHERE id = ?", (cache_id,))
        conn.commit()
        conn.close()
        return {
            "cache_id": cache_id,
            "response": response,
            "model_name": model_name,
            "similarity": round(best_score, 3),
            "is_exact": False
        }

    conn.close()
    return None

def store_in_cache(
    prompt: str, 
    response: str, 
    agent_name: str = "orchestrator", 
    model_name: str = "gpt-4o",
    tokens_saved: int = 0,
    cost_saved_usd: float = 0.0
):
    """Stores a new prompt-response pair in the semantic cache."""
    init_cache_table()
    prompt_hash = _compute_hash(prompt)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT OR REPLACE INTO semanticcache 
            (prompt_hash, prompt_text, response_text, agent_name, model_name, hit_count, tokens_saved, cost_saved_usd)
            VALUES (?, ?, ?, ?, ?, 0, ?, ?)
        """, (prompt_hash, prompt, response, agent_name, model_name, tokens_saved, cost_saved_usd))
        conn.commit()
    except Exception as e:
        print(f"⚠️ Cache insert error: {e}")
    finally:
        conn.close()

def get_cache_metrics() -> Dict[str, Any]:
    """Retrieves global semantic cache performance metrics."""
    init_cache_table()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            COUNT(*) as total_cached_items,
            SUM(hit_count) as total_hits,
            SUM(tokens_saved * hit_count) as total_tokens_saved,
            SUM(cost_saved_usd * hit_count) as total_cost_saved_usd
        FROM semanticcache
    """)
    row = cursor.fetchone()
    conn.close()

    total_items = row[0] or 0
    total_hits = row[1] or 0
    tokens_saved = row[2] or 0
    cost_saved = round(row[3] or 0.0, 6)

    return {
        "total_cached_items": total_items,
        "total_hits": total_hits,
        "total_tokens_saved": tokens_saved,
        "total_cost_saved_usd": cost_saved
    }
