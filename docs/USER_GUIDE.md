# 📘 Neuro-Symbolic Agent System — End-User Operating Manual & System Guide

**System Version**: 1.2.0 (SOTA Edition)  
**Architecture**: 5-Layer Neuro-Symbolic Hybrid Architecture  
**Repository**: [github.com/Alihanesentas/agent_system](https://github.com/Alihanesentas/agent_system)

---

## 🌟 1. INTRODUCTION & CORE PHILOSOPHY

The **Neuro-Symbolic Multi-Agent System** is an autonomous engineering operating system designed for hardware designers, firmware developers, mechanical engineers, and R&D teams.

### The Neuro-Symbolic Paradigm
Traditional LLM agents rely entirely on probabilistic model calls for every calculation, leading to high token costs ($$$$), slow response latencies, and frequent mathematical/physical hallucinations. 

Our system solves this by coupling LLM high-level reasoning with **Deterministic 0-Token ($0.00 Cost) Local Symbolic Python Engines**:
- **High-Level Reasoning (Neuro)**: Handled by Orchestrator LLMs (*Claude 3.5 Sonnet / GPT-4o*).
- **Physical & Mathematical Execution (Symbolic)**: Handled locally by 60+ Python engines (*SPICE simulation, KiCad DRC, OpenSCAD 3D CAD, thermal analysis, pinout conflict auditing, C++ static analysis*) at **$0.00 token cost in 0.1ms**.

---

## 🚀 2. HOW TO INTERACT WITH THE SYSTEM

You can interact with the system through 4 primary entry points:

### 1. Global ZSH REPL Terminal Shell (Primary Interface)
Simply type `agent` in any terminal window on your machine:
```bash
$ agent
```
- **Tab Auto-Completion**: Press `TAB` to auto-complete commands.
- **Thinking Process Box**: Displays live model reasoning steps visually.
- **Theme Manager**: Switch color palettes dynamically via `/theme matrix` or `/theme dracula`.

### 2. VSCode & Cursor IDE Sidebar Extension (v1.2.0)
- Access tree simulation monitors, autonomous goal triggers, and 5-layer pipeline visualizations directly inside your code editor sidebar.

### 3. React Web Analytics & Interactive 3D Dashboard
- Open `http://localhost:5173` in your browser.
- Real-time token expenditure graphs, 5-layer health diagnostics, **Interactive Assistant Chat Module (💬)**, and a **360° 3D Interactive PCB & Enclosure Canvas Renderer (🧊)**.

### 4. Model Context Protocol (MCP) Sunucu 2.0 (`mcp_server.py`)
- Integrated into **Claude Desktop** and **Cursor IDE**. Exposes all 58+ symbolic tools over JSON-RPC 2.0.

---

## ⚡ 3. SYSTEM OPERATING MODES

### Mode A: Autonomous Natural Language Mode (Recommended)
You **do NOT need to remember or type manual slash (`/`) commands**. Simply state your engineering goal in plain English or Turkish:

> **User Prompt**: *"Design an ESP32-S3 IoT smart home hub with battery management, 3D printed enclosure, and C++ firmware."*

#### What Happens Under the Hood Automatically:
1. **`mcu_selector.py`**: Auto-picks `ESP32-S3` based on wireless and processing requirements.
2. **`project_gen.py`**: Creates a unified project directory structure (`auto_esp32_s3/...`).
3. **`pinout.py` & `thermal.py`**: Audits GPIO pins for conflicts and verifies thermal junction temperatures locally ($0.00 cost).
4. **`layer_stackup.py` & `pcb_drc.py`**: Calculates 4-layer FR-4 dielectric stackup, 90Ω USB 2.0 trace width, and factory DRC rules.
5. **`mechanical.py` & `fasteners.py` & `gasket_sizer.py`**: Generates OpenSCAD 3D CAD enclosure, M3 screw bosses, and IP67 waterproof gasket grooves.
6. **`power_profiler.py` & `static_analyzer.py` & `ota_verifier.py`**: Synthesizes C++ firmware, audits memory leak security, calculates battery lifespan (days), and verifies SHA-256 binary headers.
7. **`report_generator.py`**: Generates a complete multidisciplinary engineering Markdown report (`.md`).

---

### Mode B: Direct Slash Command Execution (Manual Override)
For specific, one-off engineering queries, you can invoke any of the 58+ symbolic engines directly using slash commands:

#### Donanım & PCB Elektronik Komutları
- `/mcu <requirements>`: Recommends optimal MCU based on project specs.
- `/drc <trace_width>`: Audits PCB DRC factory rules and 50Ω microstrip impedance.
- `/autoroute`: Auto-routes KiCad PCB netlist traces using A* algorithm.
- `/spice <R> <C>`: Simulates RC low-pass filter frequency response.
- `/spice-transpile`: Converts KiCad schematic netlists to raw SPICE `.cir` files.
- `/pinout <pins>`: Checks ESP32 pinout conflicts and strapping pin risks.
- `/thermal <Vin> <Vout> <A>`: Calculates junction temperature rise and heatsink rating (°C/W).
- `/stackup [layers]`: Calculates 2/4/6/8-layer dielectric stackup geometry.
- `/3d-clearance`: Audits KiCad 3D STEP component height clearance against lid.
- `/footprint-check`: Cross-checks schematic symbol pins vs PCB pad layouts.
- `/trace-matching`: Calculates differential pair length matching and serpentine waves.
- `/genetic-hw`: Runs 50-generation Pareto genetic optimization for PCB routing, thermal, and cost.

#### Gömülü Yazılım & Firmware Komutları
- `/heal <file.c>`: Runs self-healing compilation error fix loop.
- `/hil <file.bin>`: Runs Hardware-in-the-Loop physical serial board tests.
- `/unittest-gen <mod>`: Generates Unity C unit test files.
- `/edge-ai <params>`: Calculates TinyML model SRAM/Flash memory and wraps ESP-DL C++ code.
- `/security <code>`: Audits C++ code for memory leaks, buffer overflows, and hardcoded secrets.
- `/coverage`: Reports C++ unit test line and branch LCOV coverage.
- `/stack-guard`: Calculates safe FreeRTOS task stack size.
- `/power <code>`: Profiles active vs deep-sleep current draw (mA) and battery life (days).
- `/watchdog`: Analyzes CPU panic crash dumps and EXCCAUSE register codes.

#### Mekanik CAD & Üretim Komutları
- `/cad <L> <W> <H>`: Generates parametric OpenSCAD 3D enclosure script.
- `/fasteners [M2-M4]`: Sizes 3D printed screw boss pilot holes and outer wall OD.
- `/snap-fit`: Calculates 3D printed cantilever snap-fit joint deflection and strain.
- `/flexure`: Calculates compliant living hinge bend radius and fatigue limits.
- `/gasket`: Sizes IP67 waterproof rubber O-ring gasket gland grooves.
- `/cable-gland`: Sizes waterproof cable gland panel cutout holes (PG7-PG9).
- `/airflow`: Calculates ventilation slot surface area (mm²) and CFM fan specs.
- `/fea [force_N]`: Simulates 3D enclosure mechanical stress (MPa) and deformation.
- `/supply-risk`: Audits BOM parts for EOL risk and global distributor stock.
- `/report`: Exports full multidisciplinary Markdown project report.
- `/slides`: Exports interactive dark-themed HTML presentation deck (`presentation.html`).

#### Güvenilirlik & Altyapı Komutları
- `/voice <prompt>`: Hands-free voice assistant workbench listener.
- `/graph <query>`: Queries Hardware Knowledge Graph for MCU/sensor relationships.
- `/reflect <task>`: Executes task with self-reflective failure critique loop.
- `/cost <prompt>`: Routes task to lowest-cost capable model.
- `/guard <code>`: Sanitizes code before writing to disk.
- `/reload-plugins`: Hot-reloads custom Python plugins from `plugins/`.
- `/circuit-breaker`: Monitors LLM API failure fallback status.
- `/budget`: Tracks monthly token expenditure dollar budget ($).
- `/dspy`: Compiles DSPy-style prompt optimization with few-shot exemplars.
- `/fsm`: Displays agent Finite State Machine status and triggers rollback.
- `/prune <text>`: Prunes prompt context for 60% token savings.
- `/compact-memory`: Compacts SQLite memory logs and vector store embeddings.

---

## 🛠️ 4. STEP-BY-STEP USER WORKFLOWS

### Workflow 1: Building a New Multidisciplinary Product
1. Open terminal and run `agent`.
2. Type your high-level goal in natural language:
   ```zsh
   agent> ESP32-S3 ile sıcaklık sensörlü, pil ile çalışan, su geçirmez kutulu cihaz yap
   ```
3. Watch the **Thinking Process Box** and **0-Token Python Execution Trace** in real time.
4. Open the generated project folder (`auto_esp32_s3_xxxx/`) to access your KiCad schematics, C++ firmware, OpenSCAD 3D enclosure, and Markdown report!

### Workflow 2: Debugging Firmware Build Errors (Self-Healing)
1. If your C++ firmware fails to compile:
   ```zsh
   agent> /heal firmware/main.cpp
   ```
2. The Self-Healing Engine captures `gcc` / `platformio` error tracebacks, identifies the broken function contract, modifies the C++ code, and re-compiles automatically until 100% build pass is achieved.

### Workflow 3: Running Physical Hardware-in-the-Loop (HIL) Tests
1. Connect your ESP32 or STM32 development board to USB.
2. Run:
   ```zsh
   agent> /hil firmware/firmware.bin
   ```
3. The system flashes the binary via `esptool`, opens the serial monitor, sends test assertions, and verifies physical hardware pin toggles.

---

## ❓ 5. FREQUENTLY ASKED QUESTIONS (FAQ)

**Q: Do I need to pay for tokens when running hardware calculations (SPICE, DRC, CAD, Thermal)?**  
**A:** No! All physical, mathematical, and CAD calculations run locally on your machine using 0-Token Python Engines at **$0.00 token cost**.

**Q: Can I use this system offline?**  
**A:** Yes! All local Python engines (KiCad parser, DRC audit, OpenSCAD CAD, SPICE, pinout checker) run 100% offline without internet connection.

**Q: Where can I see the complete command list?**  
**A:** Refer to **[docs/MASTER_FUNCTIONAL_MANUAL.md](MASTER_FUNCTIONAL_MANUAL.md)** or type `/help` inside the `agent` CLI shell.
