"""
Interactive Terminal TUI Dashboard Component.
Renders real-time hardware, database, memory, and active daemon statuses.
"""

from typing import Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from core.infra.longmem import get_memory_stats
from core.infra.rag import get_index_stats
from core.infra.service import is_port_open

console = Console()

def render_tui_dashboard():
    """Renders a comprehensive TUI status panel inside the terminal."""
    table = Table(title="🖥️ AUTONOMOUS AGENT SYSTEM TUI DASHBOARD", border_style="cyan")
    table.add_column("System Service", style="bold yellow")
    table.add_column("Status / Port", style="bold green")
    table.add_column("Metrics / Stats", style="white")

    # Backend
    b_status = "Active ✅ (Port 8000)" if is_port_open("127.0.0.1", 8000) else "Offline ❌"
    table.add_row("FastAPI Token Tracer", b_status, "SQLite tracker.db")

    # Frontend
    f_status = "Active ✅ (Port 5173)" if is_port_open("127.0.0.1", 5173) else "Offline ❌"
    table.add_row("React Web Dashboard", f_status, "http://127.0.0.1:5173")

    # RAG Index
    rag_stats = get_index_stats()
    table.add_row("RAG Vector Engine", "Active ✅", f"{rag_stats.get('total_chunks', 0)} chunks indexed (ChromaDB)")

    # Long-Term Memory
    mem_stats = get_memory_stats()
    table.add_row("Long-Term Memory", "Active ✅", f"{mem_stats.get('total_entries', 0)} decisions stored (SQLite)")

    console.print(Panel(table, border_style="cyan", padding=(1, 1)))
