"""
Rich Visual Terminal Engine for Interactive Agent CLI (Gemini & Claude CLI Style).
Renders badges, collapsible thinking boxes, extension UI panels, interactive documentation, 
and split side-by-side terminal streams for parallel agent execution using `rich`.
"""

import sys
import os
import time
from typing import Dict, Any, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.markdown import Markdown
from rich.live import Live
from rich.layout import Layout
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
try:
    from rich.collapsible import Collapsible
except ImportError:
    Collapsible = None

console = Console()

AGENT_BADGES = {
    "orchestrator": ("🧠 ORCHESTRATOR", "bold magenta", "🎯 Master Task Coordinator"),
    "planner": ("📋 PLANNER", "bold cyan", "📝 Architectural Planner"),
    "software": ("💻 SOFTWARE", "bold green", "⚡ C/C++/Python Firmware Engineer"),
    "electronics": ("⚡ ELECTRONICS", "bold yellow", "🔌 PCB & Hardware Specialist"),
    "reviewer": ("🧐 REVIEWER", "bold red", "🔍 AST Code Quality & Syntax Auditor"),
    "tutor": ("🎓 TUTOR", "bold blue", "📚 Educational Explainer")
}

MODEL_BADGES = {
    "gpt-4o": ("OpenAI gpt-4o", "green"),
    "gpt-4o-mini": ("OpenAI gpt-4o-mini", "dim green"),
    "claude-3-5-sonnet": ("Anthropic Claude 3.5 Sonnet", "yellow"),
    "gemini-1.5-flash": ("Google Gemini 1.5 Flash", "blue"),
    "llama3": ("Local Ollama (Llama-3)", "magenta")
}

def print_cli_banner():
    """Renders a sleek, modern banner styled after Gemini CLI & Claude Code."""
    banner_text = Text()
    banner_text.append("🤖 MULTI-AGENT AUTONOMOUS SYSTEM CLI\n", style="bold cyan")
    banner_text.append("SOTA Multidisciplinary Engineering Shell  •  v2.5 High Efficiency Edition\n", style="dim white")
    banner_text.append("Active Features: ", style="dim grey")
    banner_text.append("RAG Vector Engine • KiCad Tools • Vision Base64 • DAG Pipeline • Unit Testing", style="bold yellow")

    panel = Panel(
        banner_text,
        title="[bold green]⚡ AGENT SYSTEM REPL[/bold green]",
        subtitle="[dim]Type [bold yellow]/help[/bold yellow] for commands  |  Type [bold yellow]/docs[/bold yellow] for interactive manual[/dim]",
        border_style="cyan",
        padding=(1, 2)
    )
    console.print(panel)

def print_agent_status_header(agent_name: str, model_name: str, memory_status: str = "Active"):
    """Displays prompt badge header showing active Agent persona and Model."""
    agent_info = AGENT_BADGES.get(agent_name.lower(), (f"🤖 {agent_name.upper()}", "bold cyan", "Sub-Agent"))
    model_info = MODEL_BADGES.get(model_name.lower(), (model_name, "white"))

    table = Table.grid(expand=True)
    table.add_column(justify="left")
    table.add_column(justify="right")

    left = Text()
    left.append("Agent: ", style="dim white")
    left.append(f"[{agent_info[0]}] ", style=agent_info[1])
    left.append(f"({agent_info[2]})", style="dim grey")

    right = Text()
    right.append("Model: ", style="dim white")
    right.append(f"[{model_info[0]}] ", style=model_info[1])
    right.append(f"• Memory: {memory_status}", style="dim green")

    table.add_row(left, right)
    console.print(Panel(table, border_style="dim blue", padding=(0, 1)))

def render_thinking_box(reasoning_steps: List[str], final_response: str, agent_name: str = "orchestrator", elapsed_ms: float = 0.0):
    """
    Renders a transparent Thinking Process Box (Claude CLI / Gemini CLI style)
    with collapsible reasoning details and formatted Markdown final response.
    """
    agent_label = AGENT_BADGES.get(agent_name.lower(), (agent_name.upper(), "cyan", ""))[0]

    # 1. Thinking Box (Reasoning & Log Trace)
    thinking_text = Text()
    for step in reasoning_steps:
        thinking_text.append(f"  💭 {step}\n", style="dim cyan")
    thinking_text.append(f"  ⏱️ Execution Latency: {elapsed_ms}ms  |  Status: Clean Success", style="dim green")

    thinking_panel = Panel(
        thinking_text,
        title=f"[dim cyan]┌─ 💭 Thinking Process ({agent_label}) ────────────┐[/dim cyan]",
        subtitle="[dim]Press Enter to expand/collapse trace[/dim]",
        border_style="dim cyan",
        padding=(0, 1)
    )
    console.print(thinking_panel)

    # 2. Main Response Box
    md_content = Markdown(final_response)
    response_panel = Panel(
        md_content,
        title=f"[bold green]🤖 [{agent_label} Response][/bold green]",
        border_style="green",
        padding=(1, 2)
    )
    console.print(response_panel)

def render_extensions_ui(plugins_list: List[Dict[str, str]]):
    """Dedicated interactive UI panel for managing system extensions & plugins."""
    table = Table(title="🔌 EXTENSIONS & PLUGINS MANAGEMENT", border_style="cyan", header_style="bold yellow")
    table.add_column("Plugin Name", style="bold green")
    table.add_column("Category", style="magenta")
    table.add_column("Description", style="white")
    table.add_column("Status", style="bold cyan")

    if not plugins_list:
        table.add_row("No plugins registered", "-", "Add .py plugins to plugins/ directory", "Disabled")
    else:
        for p in plugins_list:
            table.add_row(p.get("name", "N/A"), p.get("category", "tool"), p.get("description", ""), "Active ✅")

    console.print(Panel(table, border_style="cyan", padding=(1, 1)))

def render_docs_ui(category: Optional[str] = None):
    """Interactive CLI Documentation Manual Viewer."""
    title = f"📖 INTERACTIVE AGENT SYSTEM MANUAL ({category.upper() if category else 'ALL MODULES'})"

    docs = {
        "rag": (
            "📚 RAG (Retrieval-Augmented Generation) Vector Engine",
            "• `/index <path>`: Index PDF datasheets, C/C++ source code, or markdown files into ChromaDB.\n"
            "• `/search <query>`: Perform semantic search over indexed documents with cosine relevance scores.\n"
            "• `/rag-stats`: View total indexed vector chunks and storage path."
        ),
        "electronics": (
            "🔌 KiCad & PCB Electronics Tools",
            "• `/kicad <file.kicad_sch>`: Parse S-expressions, components, references (R1, C1), and net labels.\n"
            "• `/kicad-set <file> <ref> <val>`: Safely update component value directly in schematic file.\n"
            "• `/bom <file.csv>`: Parse PCB Bill of Materials CSV line items.\n"
            "• `/vision <image_path>`: Encode schematic diagram PNG/JPG to Base64 for Vision LLMs."
        ),
        "components": (
            "🔍 Component Search & API Integration",
            "• `/part <part_number>`: Search Mouser/DigiKey/LCSC for stock, pricing, package, and datasheets.\n"
            "• `/alt <part_number>`: Find in-stock & drop-in alternative components.\n"
            "• `/compare <p1> <p2>`: Side-by-side parametric comparison of electronic components."
        ),
        "pipeline": (
            "🔀 Multi-Agent DAG Pipeline & Build Execution",
            "• `/pipeline <task>`: Run DAG workflow (Planner → [Hardware + Software] → Reviewer).\n"
            "• `/run <command>`: Safely execute shell build commands (gcc, make, platformio).\n"
            "• `/remember <cat> <key> <val>`: Store long-term project decisions in SQLite.\n"
            "• `/recall [cat]`: Recall project decisions across agent restarts."
        ),
        "test": (
            "🧪 Agent Unit Testing & Quality Assurance",
            "• `/test`: Run automated test suite asserting keyword presence, valid JSON, and syntax error checks."
        ),
        "sota": (
            "🚀 SOTA Donanım & Üretim Araçları",
            "• `/heal <file.c>`: Autonomous self-healing compilation error recovery loop.\n"
            "• `/spice <r> <c>`: Simulate RC circuit frequency response & step voltage.\n"
            "• `/pinout <sda> <scl> <out>`: Check GPIO pin conflicts & ESP32 strapping hazards.\n"
            "• `/flash <file.bin>`: Flash firmware binary to MCU via USB/TTY (esptool/st-flash).\n"
            "• `/serial [port]`: Read live UART serial console logs.\n"
            "• `/gerber <folder>`: Analyze PCB Gerber layers & 3D enclosure bounds."
        ),
        "mcp": (
            "🔌 Model Context Protocol (MCP) Mode & Server",
            "• `/mcp-mode <on|off>`: Toggle between Direct Native Execution (fastest, 0% token overhead) and MCP Stdio Protocol.\n"
            "• `/mcp`: Display MCP Server configuration guide for Claude Desktop & Cursor."
        ),
        "auto": (
            "🤖 Otonom Hedef Döngüsü & 5 Katmanlı Mimari",
            "• `/auto <hedef>`: Fully autonomous goal execution loop (Auto-Plan -> HW -> SW -> Thermal -> CAD -> Build).\n"
            "• `/layers <hedef>`: Execute task via explicit 5-Layer Architecture Engine."
        ),
        "tree": (
            "🌲 Agent Ağaç Hiyerarşisi & Canlı Simülasyon",
            "• `/tree [hedef]`: Display static 5-layer agent tree blueprint or launch live interactive simulation."
        )
    }

    if category and category.lower() in docs:
        selected_docs = {category.lower(): docs[category.lower()]}
    else:
        selected_docs = docs

    for cat_key, (cat_title, content) in selected_docs.items():
        console.print(Panel(Markdown(content), title=f"[bold yellow]{cat_title}[/bold yellow]", border_style="cyan", padding=(1, 2)))

def render_parallel_execution(agents_data: List[Dict[str, Any]]):
    """
    Renders split side-by-side terminal streams for parallel multi-agent execution.
    Shows simultaneous progress of multiple sub-agents (e.g. Software & Electronics).
    """
    layout = Layout()
    layout.split_row(*[Layout(name=f"agent_{i}") for i in range(len(agents_data))])

    for i, data in enumerate(agents_data):
        agent_name = data.get("name", "Agent")
        status = data.get("status", "Running")
        output = data.get("output", "")
        badge = AGENT_BADGES.get(agent_name.lower(), (agent_name.upper(), "cyan", ""))[0]

        border = "green" if status == "success" else "yellow"
        content = f"[bold]{badge}[/bold]\nStatus: {status}\n\n[dim]{output[:400]}[/dim]"

        panel = Panel(content, title=f"Stream #{i+1}: {agent_name.upper()}", border_style=border)
        layout[f"agent_{i}"].update(panel)

    console.print(layout)
