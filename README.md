# ⚡ Multi-Agent Token Tracer & Autonomous System

A powerful **Multi-Agent Framework** with an integrated **Real-Time Token Tracer System**, **Prompt Optimizer**, **Semantic Cache Engine**, **Critic Sub-Agent**, **Model Cascading Router**, **Interactive Terminal CLI Shell**, and a **Modern Dark-Mode Web Dashboard**.

Designed to measure, visualize, and benchmark LLM token usage, execution latency, and cost savings across agent developments and prompt iterations.

---

## 🏗️ System Architecture

```
                               ┌────────────────────────────────────────┐
                               │  Interactive Agent CLI (agent.py)      │
                               │  Terminal CLI (cli.py)                 │
                               │  Pure Shell Utility (tracer.sh)        │
                               └──────────────────┬─────────────────────┘
                                                  │
                                                  ▼
┌─────────────────────────┐            ┌────────────────────────────────┐
│ React + Vite Dashboard  │ ◄───────── │ FastAPI Backend (Port 8000)    │
│ (subagent_tracker/      │  REST API  │ (subagent_tracker/backend/)   │
│  frontend/)             │            └──────────────┬─────────────────┘
└─────────────────────────┘                           │
                                                      ▼
                                       ┌────────────────────────────────┐
                                       │ Peewee ORM + SQLite            │
                                       │ (tracker.db + tiktoken engine) │
                                       └────────────────────────────────┘
```

---

## ✨ Features & SOTA Multi-Agent Enhancements

- **⚡ Real-time Token & Cost Tracking**: Calculates prompt and completion token counts using `tiktoken` (`cl100k_base`) with live model cost estimations (`gpt-4o`, `gpt-4o-mini`, `claude-3-5-sonnet`, `gemini-1.5-flash`).
- **🎯 Semantic Cache Engine (`core/cache.py`)**: Stores previous prompt-response pairs using exact SHA-256 and fuzzy Jaccard similarity ($\ge \%88$) matching. Returns instant responses in **<1ms** with **0 new tokens**!
- **🧐 Critic / Reviewer Sub-Agent (`agents/reviewer.md` & `core/reviewer.py`)**: Multi-agent cross-verification engine performing AST static code analysis to catch syntax bugs and auto-correct errors.
- **🔀 Model Cascading Router (`core/router.py`)**: Analyzes task complexity (`low`, `medium`, `high`) and intelligently routes tasks to lightweight models (`gpt-4o-mini`, `gemini-1.5-flash`) for up to **%95 cost reduction**.
- **📋 Structured JSON Output Enforcer (`core/schemas.py`)**: Formats agent outputs into compact JSON, eliminating conversational fluff and reducing completion tokens by **%45+**.
- **🚀 Automated Prompt Optimizer (`core/optimizer.py`)**: Removes conversational filler, deduplicates instructions, and collapses redundant whitespace while protecting code blocks—measuring exact token & cost savings %.
- **🤖 Autonomous REPL Terminal Shell (`agent.py`)**: Gemini CLI & Claude CLI style terminal shell with interactive prompt routing, file read/write tools, model switching, and slash commands.
- **💻 Cross-Platform Terminal CLI (`cli.py`)**: Works on Linux, macOS, and Windows. Commands for `stats`, `logs`, `watch` (live refresh), `export` (CSV), and `test`.
- **🐚 Pure Shell Utility (`tracer.sh`) & Single-Line Aliases**: Native `sqlite3` terminal queries for zero-dependency log tracking (`agent-stats`, `agent-logs`, `agent-watch`, `agent-export`).
- **📊 Modern Glassmorphism Web Dashboard**: React 19 + Vite dashboard featuring live KPI cards, log detail drawer, agent token distribution progress bars, and benchmark session comparison tool.

---

## 🚀 Quick Start

### 1. Installation & Environment Setup

```bash
# Clone the repository
git clone https://github.com/Alihanesentas/agent_system.git
cd agent_system

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies and CLI package
pip install -r requirments.txt
pip install -e .
```

### 2. Single-Line Shell Aliases Setup

Source the shell setup script to load global terminal commands (`agent`, `agent-stats`, `agent-logs`, `agent-watch`, `agent-export`):

```bash
source setup_shell.sh
```

---

## 🖥️ Usage Guide

### 1. Interactive Agent CLI Shell (`agent`)

Launch the interactive REPL shell directly in your terminal:

```bash
$ agent
```

#### Slash Commands Reference:
| Slash Command | Description |
| :--- | :--- |
| `/help` | Display available interactive commands |
| `/agent <name>` | Switch active sub-agent (`orchestrator`, `planner`, `software`, `reviewer`, `tutor`) |
| `/model <name>` | Switch model (`gpt-4o`, `gpt-4o-mini`, `claude-3-5-sonnet`, `gemini-1.5-flash`) |
| `/read <path>` | Read contents of a file in your project directory |
| `/write <path> <text>` | Write or update code in a file |
| `/list [path]` | List files in project directory |
| `/stats` | View live token, cost, and latency statistics |
| `/logs` | View recent activity trace logs |
| `/clear` | Clear terminal screen |
| `/exit` | Exit interactive shell |

---

### 2. Terminal CLI Commands (`cli.py` / `tracer.sh`)

```bash
# Display summary metrics table
python cli.py stats
# OR via shell
agent-stats

# View recent trace logs
python cli.py logs --limit 10
# OR via shell
agent-logs

# Live terminal monitoring mode (auto-refresh every 3s)
python cli.py watch --interval 3
# OR via shell
agent-watch

# Export trace activity to CSV
python cli.py export --output report.csv
# OR via shell
agent-export
```

---

### 3. Web Dashboard

```bash
# Start FastAPI backend (Port 8000)
PYTHONPATH=. uvicorn subagent_tracker.backend.main:app --host 127.0.0.1 --port 8000 &

# Start React Frontend (Port 5173)
cd subagent_tracker/frontend
npm run dev -- --host 127.0.0.1
```

Open `http://127.0.0.1:5173` in your browser.

---

## 🧪 Advanced SOTA Utility Modules

### 1. Semantic Cache Engine (`core/cache.py`)
```python
from core.cache import find_cached_response, store_in_cache

# Search cache for identical/fuzzy prompt
cached = find_cached_response("Write quicksort in python", agent_name="software")
if cached:
    print(f"Instant response (<1ms, 0 tokens): {cached['response']}")
```

### 2. Critic / Reviewer Cross-Verification (`core/reviewer.py`)
```python
from core.reviewer import review_and_verify

result = review_and_verify("Print hello", "def hello(): print('World')")
print(result['status'])  # 'passed'
```

### 3. Model Cascading Router (`core/router.py`)
```python
from core.router import route_agent_task

route_info = route_agent_task("Format json text")
print(route_info['recommended_model'])  # 'gpt-4o-mini' (95% cost reduction)
```

---

## 📡 API Reference (`http://127.0.0.1:8000`)

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/log` | `POST` | Ingests agent telemetry, computes tokens/cost, and stores log |
| `/api/stats` | `GET` | Returns aggregated metrics, token breakdown by agent & model |
| `/api/cache/stats` | `GET` | Returns semantic cache hits and token savings metrics |
| `/api/logs` | `GET` | Paginated search across trace activity logs |
| `/api/export/csv` | `GET` | Exports activity logs to CSV format |
| `/api/sessions` | `POST` / `GET` | Manage benchmark test sessions |
| `/api/logs/clear` | `DELETE` | Clears all activity logs |

---

## 📁 Repository Structure

```
agent_system/
├── agent.py                      # Interactive Autonomous Agent REPL Shell
├── cli.py                        # Cross-Platform Python Terminal CLI
├── tracer.sh                     # Pure Shell Utility (sqlite3 queries)
├── setup_shell.sh                # Zsh/Bash single-line aliases setup
├── setup.py                      # Package installer & CLI entrypoints
├── requirments.txt               # Python package dependencies
├── agents/                       # Agent Prompt Specifications
│   ├── orchestrator.md
│   ├── planner.md
│   ├── software.md
│   └── reviewer.md
├── core/                         # Agent Execution Core
│   ├── runner.py                 # Runner & @trace_agent decorator
│   ├── optimizer.py              # Automated Prompt Optimizer
│   ├── cache.py                  # Semantic Cache Engine
│   ├── reviewer.py               # Critic/Reviewer Cross-Verification
│   ├── router.py                 # Model Cascading Router
│   └── schemas.py                # Structured JSON Schema Enforcer
└── subagent_tracker/             # Tracker Application
    ├── backend/                  # FastAPI + Peewee SQLite Engine
    │   ├── database.py
    │   ├── tracker.py
    │   └── main.py
    └── frontend/                 # React 19 + Vite Dark-Mode Dashboard
        ├── src/
        │   ├── App.jsx
        │   └── index.css
        └── package.json
```

---

## 📄 License
MIT License. Built for multi-agent efficiency tracking and autonomous development.
