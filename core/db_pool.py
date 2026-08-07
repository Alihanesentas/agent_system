"""
Database Connection Pool Manager Module.
Implements thread-safe connection pooling for SQLite / PostgreSQL operations.
"""

import os
import sqlite3
from queue import Queue
from typing import Dict, Any

class SQLiteConnectionPool:
    def __init__(self, db_path: str, max_connections: int = 5):
        self.db_path = db_path
        self.max_connections = max_connections
        self.pool: Queue = Queue(maxsize=max_connections)
        self._init_pool()

    def _init_pool(self):
        for _ in range(self.max_connections):
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.pool.put(conn)

    def get_connection(self) -> sqlite3.Connection:
        return self.pool.get()

    def return_connection(self, conn: sqlite3.Connection):
        self.pool.put(conn)

db_path = os.path.join(os.path.dirname(__file__), "..", "subagent_tracker.db")
global_db_pool = SQLiteConnectionPool(db_path=db_path, max_connections=5)
