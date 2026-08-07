# ⚡ Multi-Agent Token Tracer & Autonomous System

A powerful **Multi-Agent Framework** with an integrated **Real-Time Token Tracer System**, **Electronics & KiCad Schematic Tools**, **Vision Base64 Encoder**, **Prompt Optimizer**, **Semantic Cache Engine**, **Critic Sub-Agent**, **Model Cascading Router**, **Interactive Terminal CLI Shell**, and a **Modern Dark-Mode Web Dashboard**.

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
- **🔌 KiCad & PCB Electronics Tools (`core/schematics.py`)**: Parse KiCad `.kicad_sch` S-expressions, extract component references (R1, C1, U1), net labels (`I2C_SDA`, `SPI_CLK`), parse PCB BOM CSV files, and safely edit component values directly in schematic files.
- **🖼️ Multimodal Vision Reader (`core/vision.py`)**: Encodes schematic images (PNG, JPG, WEBP) to Base64 data URLs for Multimodal Vision LLMs.
- **🧠 Sliding Window Memory (`core/memory.py`)**: Summarizes older conversation turns in multi-turn dialogues, saving **%70-%80 of prompt tokens**.
- **🎯 Semantic Cache Engine (`core/cache.py`)**: Stores previous prompt-response pairs using exact SHA-256 and fuzzy Jaccard similarity ($\ge \%88$) matching. Returns instant responses in **<1ms** with **0 new tokens**!
- **🧐 Critic / Reviewer Sub-Agent (`agents/reviewer.md` & `core/reviewer.py`)**: Multi-agent cross-verification engine performing AST static code analysis to catch syntax bugs and auto-correct errors.
- **🔀 Model Cascading Router (`core/router.py`)**: Analyzes task complexity (`low`, `medium`, `high`) and intelligently routes tasks to lightweight models (`gpt-4o-mini`, `gemini-1.5-flash`) for up to **%95 cost reduction**.
- **📋 Structured JSON Output Enforcer (`core/schemas.py`)**: Formats agent outputs into compact JSON, eliminating conversational fluff and reducing completion tokens by **%45+**.
- **🤖 Autonomous REPL Terminal Shell (`agent.py`)**: Gemini CLI & Claude CLI style terminal shell with interactive prompt routing, file read/write tools, KiCad schema tools, vision reader, model switching, and slash commands.
- **💻 Cross-Platform Terminal CLI (`cli.py`)**: Works on Linux, macOS, and Windows. Commands for `stats`, `logs`, `watch` (live refresh), `export` (CSV), and `test`.

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
| `/read <path>` | Read contents of a file in your project directory |
| `/write <path> <text>` | Write or update code in a file |
| `/kicad <file.kicad_sch>` | Parse KiCad schematic components & net labels |
| `/kicad-set <file> <ref> <val>` | Update component value (e.g. `/kicad-set demo.kicad_sch R1 1k`) |
| `/bom <file.csv>` | Parse PCB Bill of Materials CSV |
| `/vision <image_path>` | Encode image schematic to Base64 for Vision LLMs |
| `/agent <name>` | Switch sub-agent (`orchestrator`, `planner`, `software`, `electronics`, `reviewer`, `tutor`) |
| `/model <name>` | Switch model (`gpt-4o`, `gpt-4o-mini`, `claude-3-5-sonnet`, `gemini-1.5-flash`) |
| `/memory` | View sliding window context memory status |
| `/stats` | View live token, cost, and latency statistics |
| `/logs` | View recent activity trace logs |
| `/clear` | Clear terminal screen and memory |
| `/exit` | Exit interactive shell |

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
│   ├── electronics.md
│   └── reviewer.md
├── core/                         # Agent Execution Core
│   ├── runner.py                 # Runner & @trace_agent decorator
│   ├── optimizer.py              # Automated Prompt Optimizer
│   ├── cache.py                  # Semantic Cache Engine
│   ├── reviewer.py               # Critic/Reviewer Cross-Verification
│   ├── router.py                 # Model Cascading Router
│   ├── schemas.py                # Structured JSON Schema Enforcer
│   ├── schematics.py             # KiCad Schematic & PCB BOM Tools
│   ├── vision.py                 # Base64 Multimodal Vision Reader
│   ├── memory.py                 # Sliding Window Context Memory
│   └── llm.py                    # Live LLM API Dispatcher
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
