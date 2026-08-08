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

- `/smps`: Calculates Buck/Boost SMPS inductor, capacitor, peak current, and efficiency.
- `/power-budget`: Computes system power budget, active vs sleep current draw (mA), and rail headroom.
- `/v-divider`: Calculates E24 standard resistor pairs for precision voltage dividers.
- `/i2c-pullup`: Calculates min/max I2C pull-up resistor values based on bus capacitance and speed.
- `/esd`: Selects IEC 61000-4-2 compliant TVS diodes and ESD protection networks.
- `/ldo-thermal`: Calculates LDO regulator power dissipation (W), junction temperature (°C), and efficiency.
- `/mosfet-driver`: Sizes MOSFET gate driver peak output current (A), switching time (ns), and gate drive power loss.
- `/analog-filter`: Designs 2nd-order active Sallen-Key low-pass/high-pass filters and calculates capacitor values.
- `/current-sense`: Calculates current sense shunt resistor (mΩ), power loss, and INA amplifier output voltage.
- `/uart-config`: Calculates UART baud rate integer/fractional clock dividers and baud error percentage.
- `/wheatstone-bridge`: Calculates Wheatstone bridge strain gauge differential output voltage (mV) and sensitivity.
- `/pcb-cost`: Estimates bare board PCB fabrication and SMT component placement batch cost ($).
- `/psu-ripple`: Calculates power supply output voltage ripple (mV), min C_out (uF), and ESR ripple contribution.
- `/spi-timing`: Analyzes SPI bus clock frequency, mode (0-3), and setup/hold time margins (ns).
- `/usb-impedance`: Audits USB 2.0 / 3.0 differential pair microstrip impedance (90Ω ± 10%).
- `/fuse-sizing`: Calculates fuse current rating and inrush energy melting integral I²t (A²s).
- `/reverse-polarity`: Compares reverse polarity protection topologies (Schottky vs P-FET vs Ideal Diode).
- `/dac-output`: Calculates DAC LSB voltage (mV), required Op-Amp slew rate (V/us), and settling time.
- `/ethernet-mag`: Calculates 10/100/1000Base-T Ethernet magnetics, Bob Smith termination, and PoE power.
- `/lvds-serdes`: Analyzes LVDS differential voltage swing (mV), common mode, and jitter budget.
- `/sensor-interface`: Designs sensor signal conditioning (PT100/NTC) and anti-aliasing RC filter.
- `/thermocouple`: Calculates Thermocouple Seebeck EMF (mV) and Cold Junction Compensation (CJC).
- `/crosstalk`: Analyzes PCB trace crosstalk (NEXT/FEXT dB) and 3W rule compliance.
- `/impedance-adv`: Calculates Microstrip/Stripline/CPWG trace impedance Z0 per IPC-2141.
- `/opamp`: Calculates Op-Amp gain (dB / V/V), feedback resistor values, input impedance, and 3dB bandwidth.
- `/adc-snr`: Calculates ADC theoretical SNR, measured ENOB, LSB size (uV), quantization noise, and Nyquist bandwidth.
- `/can-bus`: Calculates CAN bus bit timing segments (Prop/Phase1/Phase2/SJW), prescaler, and 120Ω termination.
- `/via-current`: Calculates PCB via DC current capacity (IPC-2152), via resistance, voltage drop, and thermal matrix.
- `/rtos-design`: Designs FreeRTOS task priorities, stack memory allocation, and CPU utilization.
- `/pid-tune`: Calculates Kp, Ki, Kd PID tuning parameters using Ziegler-Nichols method.
- `/modbus-gen`: Generates industrial Modbus RTU/TCP holding register maps and C struct headers.
- `/mqtt-cfg`: Generates structured IoT MQTT topic hierarchies and QoS parameters.
- `/ble-gatt`: Generates BLE GATT custom 128-bit UUID services, characteristics, and NimBLE C code.
- `/lorawan`: Calculates LoRaWAN Time-on-Air (ms), Spreading Factor (SF), sensitivity, link budget, and ETSI duty cycle.
- `/crypto`: Calculates embedded crypto accelerator throughput (Mbps), execution time, and RAM footprint.
- `/digital-filter`: Generates FIR/IIR filter tap coefficients and C header array definitions.
- `/isr-latency`: Calculates NVIC interrupt entry latency, WCET (us), and max trigger frequency.
- `/memory-pool`: Designs deterministic O(1) static fixed-block memory pools with alignment padding.
- `/ring-buffer`: Designs lock-free circular ring buffers with power-of-two mask indexing and C headers.
- `/mutex-deadlock`: Detects RTOS mutex cyclic lock dependency deadlocks and priority inversion risks.
- `/protobuf-gen`: Generates Protocol Buffers proto3 schemas and nanopb ANSI C struct headers.
- `/secure-boot`: Generates Secure Boot V2 ECDSA-P256 signing key configurations and eFuse burn commands.
- `/fatfs-config`: Calculates LittleFS / FATFS sector layout, block count, and wear leveling write endurance.
- `/misra-checker`: Audits C/C++ source code for MISRA-C:2012 safety-critical compliance rule violations.
- `/scheduler-sim`: Simulates Rate Monotonic (RMS) and EDF RTOS schedulability and CPU load limits.
- `/zigbee-mesh`: Designs Zigbee 3.0 / Thread wireless mesh node topology and RAM routing table footprint.
- `/cert-manager`: Generates X.509 CA root, client CSR certificates, and mTLS configuration commands.
- `/eeprom-wear`: Calculates EEPROM / Flash wear leveling lifetime endurance (years) and write frequency.
- `/fft-analyzer`: Calculates FFT frequency bin resolution (Hz), Nyquist frequency, and windowing loss.
- `/print-cost`: Estimates total 3D printing manufacturing cost (material, power, machine wear).
- `/motor-size`: Sizes DC/BLDC/Stepper motor torque, RPM, and mechanical power.
- `/bolt-torque`: Calculates metric bolt tightening torque (Nm) and preload force (kN) per VDI 2230.
- `/spring`: Designs helical compression springs, calculating spring rate k, Wahl factor, and shear stress.
- `/gear-ratio`: Calculates spur gear train reduction ratio, output RPM, output torque (Nm), and center distance.
- `/heatsink`: Calculates finned aluminum heatsink required thermal resistance Rth (°C/W) and volume.
- `/tolerance-stack`: Calculates Worst-Case and Root-Sum-Square (RSS) 3-sigma statistical tolerance stack-up.
- `/bearing-life`: Calculates ISO 281 ball and roller bearing L10 rating life (M-revs) and operating hours.
- `/slicer-settings`: Recommends 3D printing slicer parameters (temperatures, speeds, fans) per material.
- `/sheet-metal`: Calculates sheet metal Bend Allowance (BA in mm) and Bend Deduction (BD in mm) flat patterns.
- `/injection-mold`: Calculates injection molding material shrinkage (%), clamp force (Tons), and cooling time.
- `/cnc-feedrate`: Calculates CNC milling spindle speed (RPM), table feed rate (mm/min), and MRR (cm³/min).
- `/beam-stress`: Calculates structural beam bending moment (Nm), stress (MPa), deflection (mm), and safety factor.

- `/rest-gen`: Generates FastAPI / Express CRUD REST API router scaffolds.
- `/graphql-gen`: Generates GraphQL SDL schemas and query/mutation resolver stubs.
- `/auth-flow`: Generates OAuth2 / JWT authentication, signing algorithms, and RBAC middleware code.
- `/nginx-gen`: Generates production Nginx reverse proxy configs with SSL TLS 1.3 and rate limiting.
- `/rate-limiter`: Calculates API rate limiting token bucket capacity and Redis Lua scripts.
- `/websocket`: Generates real-time WebSocket connection manager and broadcast handler boilerplate.
- `/ci-cd`: Generates GitHub Actions / GitLab CI workflow YAML pipelines.
- `/sql-gen`: Generates PostgreSQL / SQLite DDL table schemas and indexes.
- `/terraform-gen`: Generates AWS Terraform IaC module HCL configurations.
- `/cot`: Runs Tree-of-Thought reasoning decomposition and parallel branch evaluation.
- `/health-probe`: Runs synthetic health probe checks across background DBs, workers, and services.
- `/cron-schedule`: Schedules periodic background cron jobs.
- `/env-manager`: Audits environment variables and checks required production secret keys (.env).
- `/retry-policy`: Configures exponential backoff retry schedules with randomized full jitter.


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

### Workflow 4: Building Full-Stack Web, Backend & Cloud Software
1. Open terminal and run `agent`.
2. Enter your general computer software goal in natural language:
   ```zsh
   agent> Create a production FastAPI REST backend with Docker, PostgreSQL schema, and AWS Terraform scripts
   ```
3. The system automatically triggers the zero-token software tools:
   - **`web_architecture.py`**: Generates production FastAPI REST API routers and Pydantic schemas.
   - **`db_migration.py`**: Generates PostgreSQL DDL table schemas and index optimization.
   - **`docker_k8s.py`**: Generates multi-stage Dockerfile and Kubernetes manifests.
   - **`cloud_devops.py`**: Generates AWS Terraform HCL infrastructure scripts.
   - **`uml_generator.py`**: Generates Mermaid sequence architecture diagrams.

---

## ❓ 5. FREQUENTLY ASKED QUESTIONS (FAQ)

**Q: Do I need to pay for tokens when running hardware calculations (SPICE, DRC, CAD, Thermal)?**  
**A:** No! All physical, mathematical, and CAD calculations run locally on your machine using 0-Token Python Engines at **$0.00 token cost**.

**Q: Can I use this system offline?**  
**A:** Yes! All local Python engines (KiCad parser, DRC audit, OpenSCAD CAD, SPICE, pinout checker) run 100% offline without internet connection.

**Q: Where can I see the complete command list?**  
**A:** Refer to **[docs/MASTER_FUNCTIONAL_MANUAL.md](MASTER_FUNCTIONAL_MANUAL.md)** or type `/help` inside the `agent` CLI shell.
