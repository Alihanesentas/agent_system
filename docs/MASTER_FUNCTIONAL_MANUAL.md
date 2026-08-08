# 📚 Neuro-Symbolic Agent System — Master Functional Technical Manual

**System Version**: 1.2.0 (SOTA Edition)  
**Architecture**: 5-Layer Multi-Agent & Neuro-Symbolic Hybrid Architecture  
**Repository**: [github.com/Alihanesentas/agent_system](https://github.com/Alihanesentas/agent_system)

---

## 🏛️ 1. ARCHITECTURAL DESIGN & CONTRACTS (5-LAYER ARCHITECTURE)

The system couples the high-level reasoning power of Large Language Models with deterministic 0-Token ($0.00 Cost) Local Symbolic Python Engines.

```
Layer 1 (Presentation): Rich REPL CLI, VSCode/Cursor Extension v1.2.0, React Web Analytics Dashboard (Port 5173), Stdio MCP Server 2.0.
Layer 2 (Orchestration): Claude 3.5 Sonnet / GPT-4o Orchestrator, /auto Autonomous Goal Loop, /tree Live Agent Tree Monitor.
Layer 3 (Specialist Sub-Agents): Electronics PCB Sub-Agent, Firmware C++ Sub-Agent, Mechanical 3D CAD Sub-Agent, Reviewer Sub-Agent.
Layer 4 (Symbolic Python Engines): SPICE Simulator, Pinout Auditor, Thermal Dissipation, PCB DRC & Impedance, OpenSCAD 3D Generator, USB Flasher.
Layer 5 (Persistence & Infrastructure): ChromaDB RAG Engine, SQLite Long-Term Memory, User Engineer Profile, Async Worker Queue, Token Bucket Limiter.
```

---

## 🔌 2. MODULAR PACKAGE CATALOG (`core/`)

- **`core/engine/`**: Workflow, DAG, Autonomous Goal & Simulation Engines
  - `autonomous_agent.py`: `/auto` True Goal-Driven Loop
  - `layered_architecture.py`: `/layers` 5-Layer Architectural Engine
  - `agent_tree_sim.py`: `/tree` Live Agent Tree Hierarchy Monitor
  - `dag_executor.py`: Parallel Async DAG Executor
  - `cost_router.py`: `/cost` Dynamic Model Cost Optimizer Router
  - `replay_engine.py`: `/replay` Time-Travel Execution Debugger
  - `state_machine.py`: `/fsm` Finite State Machine & Rollback Engine
  - `critical_path.py`: `/critical-path` Critical Bottleneck Path Profiler
  - `agent_telemetry.py`: `/agent-telemetry` Sub-Agent Latency Profiler
  - `prompt_template.py`: Versioned Prompt Template Engine
- **`core/hardware/`**: KiCad, PCB, SPICE & Hardware Tools
  - `schematics.py`: KiCad Schematic & Netlist S-Expression Parser
  - `spice.py`: `/spice` RC Filter Simulator
  - `spice_transpiler.py`: `/spice-transpile` KiCad Netlist to SPICE Transpiler
  - `pinout.py`: `/pinout` ESP32 Pinout Conflict & Strapping Pin Auditor
  - `thermal.py`: `/thermal` Thermal Dissipation & Heatsink Calculator
  - `pcb_drc.py`: `/drc` PCB Factory DRC Rules & 50Ω Trace Impedance
  - `autorouter.py`: `/autoroute` KiCad PCB A* Netlist Auto-Router
  - `rf_antenna.py`: `/rf` PCB Quarter-Wave Monopole Antennas & 50Ω Matching
  - `flasher.py`: `/flash` USB Firmware Flasher & Serial Monitor
  - `emc_compliance.py`: `/emc` FCC Class B & CE Certification Pre-Checker
  - `mcu_selector.py`: `/mcu` Multi-MCU Board Selector & Spec Recommender
  - `layer_stackup.py`: `/stackup` PCB Dielectric Layer Stackup Calculator
  - `kicad_3d_models.py`: `/3d-clearance` 3D Component Height Clearance Audit
  - `footprint_crosscheck.py`: `/footprint-check` Symbol vs Footprint Pad Cross-Checker
  - `trace_length_matching.py`: `/trace-matching` Differential Pair Length Matching
  - `genetic_optimizer.py`: `/genetic-hw` Multi-Objective Genetic Hardware Optimizer
  - `smps_design.py`: `/smps` Buck/Boost SMPS Converter Designer
  - `power_budget.py`: `/power-budget` System Power Consumption & Current Draw Matrix
  - `voltage_divider.py`: `/v-divider` Precision Resistor Voltage Divider Calculator
  - `i2c_pullup.py`: `/i2c-pullup` I2C Bus Pull-Up Resistor & Rise Time Calculator
  - `esd_protection.py`: `/esd` ESD Protection & TVS Diode Selector
  - `ldo_thermal.py`: `/ldo-thermal` LDO Power Loss, Junction Temp & Efficiency Calculator
  - `mosfet_driver.py`: `/mosfet-driver` MOSFET Gate Driver Peak Current & Loss Sizer
  - `filter_design.py`: `/analog-filter` Active Sallen-Key Low-pass & High-pass Filter Designer
  - `current_sense.py`: `/current-sense` Shunt Resistor & INA Current Sense Circuit Designer
  - `uart_config.py`: `/uart-config` UART Baud Rate Clock Divider & Error % Calculator
  - `wheatstone_bridge.py`: `/wheatstone-bridge` Wheatstone Bridge & Strain Gauge Calculator
  - `pcb_cost_estimator.py`: `/pcb-cost` PCB Fabrication & SMT Assembly Batch Cost Estimator
  - `psu_ripple.py`: `/psu-ripple` Power Supply Voltage Ripple & Filter Capacitor Calculator
  - `spi_timing.py`: `/spi-timing` SPI Bus Clock Timing, Mode (0-3) & Setup/Hold Analyzer
  - `usb_impedance.py`: `/usb-impedance` USB 2.0/3.0 Differential Pair 90Ω Impedance Checker
  - `fuse_sizing.py`: `/fuse-sizing` Electric Fuse Sizing & Inrush Energy Melting Integral I²t Calculator
  - `reverse_polarity.py`: `/reverse-polarity` Reverse Polarity Protection Circuit Topology Designer
  - `dac_output.py`: `/dac-output` DAC Output Buffer & Settling Time Designer
  - `ethernet_magnetics.py`: `/ethernet-mag` Ethernet PHY Magnetics & PoE Interface Designer
  - `lvds_serdes.py`: `/lvds-serdes` LVDS / SerDes High-Speed Differential Signal Integrity Analyzer
  - `sensor_interface.py`: `/sensor-interface` Analog & Digital Sensor Interface Circuit Designer
  - `thermocouple.py`: `/thermocouple` Thermocouple Cold Junction Compensation & Type Selector
  - `crosstalk_analysis.py`: `/crosstalk` PCB Trace Crosstalk (NEXT/FEXT) & Guard Trace Analyzer
  - `impedance_calculator.py`: `/impedance-adv` Advanced PCB Microstrip & Stripline Impedance Calculator (IPC-2141)
  - `panelization.py`: `/panelization` PCB Array Panelization & V-Score Breakaway Tab Optimizer
  - `gerber_checker.py`: `/gerber-checker` Gerber RS-274X Layer Set Integrity Validator
  - `pcb_thermal_relief.py`: `/thermal-relief` PCB Thermal Relief Spoke Width & Solderability Calculator
- **`core/computer/`**: Full-Stack Web, Microservices, Frontend & Computer Science Engines
  - `web_stack.py`: `/web-stack` Full-Stack FastAPI / Express REST API Generator
  - `microservices.py`: `/proto` gRPC Protobuf3 & Message Queue Bus Generator
  - `frontend_gen.py`: `/react` React Vite / Next.js TSX Component Scaffolding
  - `code_complexity.py`: `/complexity` AST Cyclomatic Code Complexity Auditor
  - `rest_api_gen.py`: `/rest-gen` REST API Router & Scaffold Generator
  - `ci_cd_pipeline.py`: `/ci-cd` CI/CD Workflow Pipeline Generator
  - `sql_schema_gen.py`: `/sql-gen` SQL DDL Schema & Migration Generator
  - `graphql_schema.py`: `/graphql-gen` GraphQL SDL Schema & Resolver Generator
  - `terraform_gen.py`: `/terraform-gen` AWS Terraform IaC Module Generator
  - `auth_flow.py`: `/auth-flow` OAuth2 / JWT Authentication & RBAC Middleware Generator
  - `nginx_config.py`: `/nginx-gen` Nginx Reverse Proxy, TLS 1.3 & Rate Limit Config Generator
  - `rate_limit_design.py`: `/rate-limiter` API Rate Limiter & Token Bucket Strategy Generator
  - `websocket_handler.py`: `/websocket` Real-Time WebSocket Connection Manager & Broadcast Generator
  - `nosql_model.py`: `/nosql-model` NoSQL Document & Key-Value Database Capacity Designer
- **`core/software/`**: Firmware, Testing, DevOps & Container Engines
  - `executor.py`: Shell Runner for gcc / make / platformio
  - `docker_k8s.py`: `/docker-gen` Dockerfile & Kubernetes Deployment Manifest Generator
  - `rtos_task_design.py`: `/rtos-design` FreeRTOS Task Priority & Stack Sizing Designer
  - `pid_tuner.py`: `/pid-tune` PID Controller Auto-Tuner
  - `modbus_gen.py`: `/modbus-gen` Modbus RTU/TCP Register Map & C Struct Generator
  - `mqtt_topic.py`: `/mqtt-cfg` MQTT Topic Hierarchy Generator
  - `ble_gatt.py`: `/ble-gatt` BLE GATT Custom UUID Service Generator
  - `lorawan_params.py`: `/lorawan` LoRaWAN Time-on-Air & Link Budget Calculator
  - `crypto_engine.py`: `/crypto` Embedded Crypto Accelerator Sizer
  - `fir_iir_filter.py`: `/digital-filter` FIR/IIR Digital Filter Tap Coefficient Generator
  - `isr_latency.py`: `/isr-latency` NVIC Interrupt Latency, WCET & Max Frequency Analyzer
  - `memory_pool.py`: `/memory-pool` Static Fixed-Block Embedded Memory Pool Designer
  - `ring_buffer.py`: `/ring-buffer` Lock-Free Circular Ring Buffer Sizer & C Code Generator
  - `mutex_deadlock.py`: `/mutex-deadlock` RTOS Mutex Deadlock & Priority Inversion Detector
  - `protobuf_gen.py`: `/protobuf-gen` Protocol Buffers Proto3 Schema & Nanopb C Struct Generator
  - `secure_boot.py`: `/secure-boot` Embedded Secure Boot V2 & Flash Encryption Configurator
  - `fatfs_config.py`: `/fatfs-config` Embedded FATFS / LittleFS Wear Leveling Configurator
  - `misra_checker.py`: `/misra-checker` MISRA-C:2012 Safety-Critical Static Compliance Analyzer
  - `scheduler_sim.py`: `/scheduler-sim` RTOS Rate Monotonic & EDF Scheduler Simulator
  - `zigbee_mesh.py`: `/zigbee-mesh` Zigbee 3.0 / Thread Wireless Mesh Topology Designer
  - `cert_manager.py`: `/cert-manager` X.509 Certificate Chain & TLS mTLS Configurator
  - `eeprom_wear.py`: `/eeprom-wear` EEPROM / Flash Wear Leveling Lifetime Endurance Analyzer
  - `fft_analyzer.py`: `/fft-analyzer` FFT Frequency Resolution & Windowing Analyzer
  - `log_framework.py`: `/log-framework` Embedded Circular Logging Framework Generator
  - `unit_test_scaffold.py`: `/unit-test` Unity C Unit Test Suite & CMock Generator
  - `code_size_analyzer.py`: `/code-size` GCC Map File Code Size & Memory Usage Analyzer
  - `firmware_diff.py`: `/firmware-diff` Firmware Binary Diff & OTA Patch Size Analyzer
- **`core/production/`**: Mechanical CAD & Manufacturing
  - `print_cost.py`: `/print-cost` 3D Printing Manufacturing Cost Estimator
  - `motor_sizing.py`: `/motor-size` Motor Torque & Power Sizing Engine
  - `bolt_torque.py`: `/bolt-torque` Bolt Tightening Torque Calculator
  - `spring_design.py`: `/spring` Helical Compression Spring Designer
  - `gear_ratio.py`: `/gear-ratio` Spur & Planetary Gear Train Calculator
  - `heatsink_design.py`: `/heatsink` Finned Aluminum Heatsink Dimensioning Engine
  - `tolerance_stack.py`: `/tolerance-stack` Worst-Case & RSS 3-Sigma Tolerance Stack-Up Analyzer
  - `bearing_life.py`: `/bearing-life` ISO 281 Ball & Roller Bearing L10 & L10h Life Calculator
  - `print_settings.py`: `/slicer-settings` 3D Printer Material Slicer Parameter Recommender
  - `sheet_metal.py`: `/sheet-metal` Sheet Metal Bend Allowance (BA) & Deduction (BD) Calculator
  - `injection_mold.py`: `/injection-mold` Plastic Injection Molding Shrinkage & Tooling Estimator
  - `cnc_feedrate.py`: `/cnc-feedrate` CNC Milling Spindle Speed & Feed Rate Calculator
  - `beam_stress.py`: `/beam-stress` Structural Beam Bending Stress & Deflection Calculator
  - `vibration_analysis.py`: `/vibration` Natural Frequency & Vibration Transmissibility Analyzer
  - `fan_selection.py`: `/fan-selection` Cooling Fan Selection & Airflow CFM Calculator
  - `pipe_flow.py`: `/pipe-flow` Fluid Pipe Flow Reynolds & Pressure Drop Calculator
  - `solenoid_design.py`: `/solenoid` Electromechanical Solenoid Force & Flyback Diode Designer
  - `linear_actuator.py`: `/linear-actuator` Linear Actuator & Lead Screw Drive Torque Calculator
  - `encoder_resolution.py`: `/encoder` Rotary & Linear Encoder Resolution Calculator
  - `enclosure_ip.py`: `/enclosure-ip` IP Rating Ingress Protection Seal Checker


- **`core/engine/`**: Orchestration & Reasoning
  - `chain_of_thought.py`: `/cot` Chain-of-Thought / Tree-of-Thought Reasoning Framework
- **`core/infra/`**: Infrastructure & Systems
  - `health_check.py`: `/health-probe` Service Health Probe Engine
  - `cron_scheduler.py`: `/cron-schedule` Periodic Background Cron Task Scheduler
  - `env_manager.py`: `/env-manager` Environment Variable & Secret Key Manager (.env)
  - `retry_policy.py`: `/retry-policy` Exponential Backoff & Jitter Retry Policy Engine




  - `cloud_devops.py`: `/devops` AWS Terraform HCL & GitHub Actions CI/CD Pipeline
  - `uml_generator.py`: `/uml` Mermaid UML Sequence Diagram Generator
  - `db_migration.py`: `/db-schema` PostgreSQL DDL Schema & SQL Migration Generator
- **`core/production/`**: CAD, Mechanical & Production Planning Tools
  - `mechanical.py`: `/cad` OpenSCAD 3D Enclosure Generator & Slicer Recommender
  - `fasteners.py`: `/fasteners` 3D Printed Screw Boss Thread Sizer (M2-M4)
  - `snap_fit.py`: `/snap-fit` Cantilever Snap-Fit Joint Strain Calculator
  - `flexure_hinge.py`: `/flexure` Living Hinge Strain & Bend Radius Calculator
  - `gasket_sizer.py`: `/gasket` IP67 Waterproof O-Ring Gasket Groove Sizer
  - `cable_gland.py`: `/cable-gland` Waterproof Cable Gland Cutout Hole Sizer
  - `airflow_calculator.py`: `/airflow` Ventilation Slot & CFM Airflow Calculator
  - `fea_simulation.py`: `/fea` 3D Mechanical FEA Stress & Deformation Simulator
  - `cart_builder.py`: `/cart` Mouser / LCSC 1-Click Shopping Cart Generator
  - `bom_optimizer.py`: `/bom-opt` BOM Cost Driver & Tier Optimizer
  - `bom_stock_tracker.py`: `/supply-risk` Multi-Vendor BOM Stock & EOL Risk Alert
  - `bom_sensitivity.py`: `/bom-sensitivity` Monte Carlo Cost Sensitivity Analyzer
  - `battery.py`: `/battery` Battery Lifespan & Solar Panel Calculator
  - `harness.py`: `/harness` Wire AWG Cross-Section & Voltage Drop Calculator
  - `gantt_planner.py`: `/gantt` Mermaid Gantt Project Schedule Generator
  - `project_gen.py`: `/create-project` Unified Project Tree Generator
  - `report_generator.py`: `/report` Full Project Markdown Report Generator
  - `presentation_exporter.py`: `/slides` Interactive HTML Presentation Exporter
- **`core/infra/`**: Infrastructure, Vector Store, Cache & Telemetry
  - `cache.py`: Semantic Cache Engine (80% Token Savings)
  - `checkpoint.py`: `/checkpoint` & `/restore` Snapshot State Backup/Restore
  - `voice_agent.py`: `/voice` Hands-Free Workbench Voice Assistant
  - `knowledge_graph.py`: `/graph` Hardware Relational Knowledge Graph
  - `self_reflection.py`: `/reflect` Self-Reflective Failure Critique Engine
  - `guardrails.py`: `/guard` Real-Time Code Output Safety Filter
  - `plugin_loader.py`: `/reload-plugins` Hot-Reloadable Plugin Loader
  - `worker_queue.py`: `/worker` Async Background Worker Queue
  - `rate_limiter.py`: `/ratelimit` LLM API Token Bucket Throttler
  - `circuit_breaker.py`: `/circuit-breaker` Multi-Model API Fallback Circuit Breaker
  - `token_budget.py`: `/budget` Token Expenditure Dollar Budget Tracker
  - `cost_forecast.py`: `/cost-forecast` LLM Token Burn Rate Forecast Engine
  - `dspy_optimizer.py`: `/dspy` DSPy Prompt Optimizer & Few-Shot Bootstrapper
  - `ensemble_aggregator.py`: `/ensemble` Multi-Model Response Ensemble Aggregator
  - `context_pruner.py`: `/prune` LLM Prompt Context Pruner (60% Savings)
  - `memory_compactor.py`: `/compact-memory` SQLite & Vector Store Memory Compactor
  - `adaptive_backoff.py`: `/backoff` API Rate Limit Exponential Backoff Calculator
  - `system_prompt_builder.py`: `/prompt-builder` Dynamic System Prompt Context Builder
  - `agent_health.py`: `/agent-health` Sub-Package Real-Time Health Monitor
  - `token_minimizer.py`: `/token-count` BPE Token Counter & Cost Estimator
  - `theme_manager.py`: `/theme` CLI Color Palette Switcher
  - `autocomplete.py`: REPL TAB Command Auto-Completer

---

## 🛠️ 3. COMPREHENSIVE SLASH COMMAND MANUAL (58+ COMMANDS)

### 🤖 Autonomous Goal & Layer Execution Commands
- **`/auto <goal>`**: Executes high-level goal completely autonomously (hardware + CAD + firmware + DRC + report).
- **`/layers <goal>`**: Step-by-step execution across 5-Layer Architecture.
- **`/tree [goal]`**: Visualizes hierarchical agent execution tree and latencies.

### 🔌 Electronics & Hardware Commands
- **`/kicad <file.kicad_sch>`**: Parses KiCad schematic components and net labels.
- **`/spice <r_ohms> <c_farads>`**: Simulates RC low-pass filter frequency response.
- **`/spice-transpile`**: Transpiles KiCad netlist to raw SPICE `.cir` file.
- **`/pinout <sda> <scl> <out>`**: Audits ESP32 pinout conflicts and strapping pin risks.
- **`/thermal <vin> <vout> <amps>`**: Calculates thermal dissipation and heatsink requirements.
- **`/drc <width_mm>`**: Audits PCB factory DRC rules and 50Ω trace impedance.
- **`/autoroute`**: Auto-routes KiCad PCB netlist traces using A* algorithm.
- **`/rf [freq_mhz]`**: Calculates PCB quarter-wave monopole antenna dimensions.
- **`/mcu <req>`**: Recommends optimal microcontroller (ESP32-S3, STM32F4, RP2040, nRF52840, Teensy 4.1).
- **`/stackup [layers]`**: Calculates PCB dielectric layer stackup and USB 2.0 90Ω trace width.
- **`/3d-clearance`**: Audits KiCad 3D STEP component height clearance against lid.
- **`/footprint-check`**: Cross-checks schematic symbol pins vs PCB footprint pads.
- **`/trace-matching`**: Calculates high-speed differential pair length matching and serpentine tuning.
- **`/genetic-hw`**: Optimizes PCB trace length, thermal dissipation, and BOM cost across 50 generations.

### 💻 Software & Firmware Commands
- **`/heal <file.c>`**: Self-healing loop for build errors.
- **`/hil <file.bin>`**: Runs Hardware-in-the-Loop physical board tests.
- **`/unittest-gen <mod>`**: Generates Unity C unit test files.
- **`/edge-ai <params>`**: Calculates TinyML SRAM/Flash memory and wraps ESP-DL C++ code.
- **`/ota [version]`**: Generates firmware OTA update manifest.
- **`/ota-verify`**: Verifies firmware binary SHA-256 signature and magic header.
- **`/watchdog`**: Analyzes CPU panic crash dumps and watchdog reset causes.
- **`/security <code>`**: Audits C++ code for memory leaks and unsafe functions.
- **`/coverage`**: Reports C++ unit test line and branch LCOV coverage.
- **`/stack-guard`**: Calculates safe FreeRTOS task stack size.
- **`/bootloader-check`**: Audits bootloader flash offset and vector table integrity.

### 🛠️ Mechanical CAD & Production Commands
- **`/cad <l> <w> <h>`**: Generates parametric OpenSCAD 3D enclosure script.
- **`/slicer <material>`**: Recommends FDM 3D printer slicer settings.
- **`/fasteners [type]`**: Sizes 3D printed screw boss pilot holes (M2-M4).
- **`/snap-fit`**: Calculates 3D printed snap-fit joint deflection and strain.
- **`/flexure`**: Calculates compliant living hinge bend radius and fatigue limits.
- **`/gasket`**: Calculates IP67 waterproof O-ring groove depth and width.
- **`/cable-gland`**: Sizes waterproof cable gland panel cutout holes (PG7-PG9).
- **`/airflow`**: Calculates ventilation slot surface area and CFM fan specs.
- **`/fea [force_N]`**: Simulates 3D enclosure mechanical stress and deformation.
- **`/cart [bom.csv]`**: Generates Mouser / LCSC 1-click shopping cart payload.
- **`/bom-opt`**: Optimizes BOM cost drivers and volume pricing tiers.
- **`/supply-risk`**: Audits BOM parts for EOL risk and global stock availability.
- **`/bom-sensitivity`**: Runs Monte Carlo simulation on BOM price swings.
- **`/gantt`**: Generates Mermaid Gantt project schedule chart.
- **`/report`**: Exports full multidisciplinary Markdown engineering report.
- **`/slides`**: Exports interactive dark-themed HTML presentation slide deck.

### 🛡️ Reliability, Security & Infrastructure Commands
- **`/voice <prompt>`**: Hands-free voice assistant workbench listener.
- **`/graph <query>`**: Queries Hardware Knowledge Graph for MCU/sensor relationships.
- **`/reflect <task>`**: Executes task with self-reflective critique loop.
- **`/cost <prompt>`**: Routes task to lowest-cost capable model.
- **`/guard <code>`**: Sanitizes code before writing to disk.
- **`/reload-plugins`**: Hot-reloads custom Python plugins from `plugins/`.
- **`/worker`**: Monitors async background worker queue.
- **`/ratelimit`**: Monitors LLM API token bucket rate limiter.
- **`/circuit-breaker`**: Monitors API failure fallback circuit breaker status.
- **`/budget`**: Tracks monthly token expenditure dollar budget.
- **`/cost-forecast`**: Forecasts monthly token cost burn rate.
- **`/dspy`**: Compiles DSPy-style prompt optimization with few-shot exemplars.
- **`/fsm`**: Monitors agent Finite State Machine and triggers rollback.
- **`/ensemble`**: Aggregates multi-model responses using majority voting.
- **`/prune <text>`**: Prunes prompt context for 60% token savings.
- **`/compact-memory`**: Compacts SQLite memory logs and vector store.
- **`/agent-health`**: Displays real-time health scores for all 5 sub-packages.
- **`/token-count <text>`**: Counts BPE tokens and estimates prompt cost.
- **`/theme <name>`**: Switches CLI color palette (cyberpunk, matrix, dracula).
- **`/smart <task>`**: LLM Smart Dispatch — ENGINE_REGISTRY'den 0-token engine arar, bulamazsa LLM fallback ile script üretir.
- **`/engines`**: Kayıtlı 50+ adet 0-token engine'in tam listesini gösterir.
- **`/generated`**: LLM'in daha önce üretip cache'lediği script'lerin listesini gösterir.
- **`/fallback-test <task>`**: Verilen görev için engine registry eşleşme testini çalıştırır.
- **`/smps`**: Buck/Boost SMPS converter indüktör, kapasitör ve verim hesabı yapar.
- **`/power-budget`**: Sistem güç bütçesi tablosu ve peak/avg mA çekimini hesaplar.
- **`/v-divider`**: Hassas E24 direnç çifti voltaj bölücü hesabı yapar.
- **`/i2c-pullup`**: I2C hattı pull-up direnci ve max yükselme süresini (rise time) hesaplar.
- **`/esd`**: IEC 61000-4-2 uyumlu TVS diyot koruma devresi seçer.
- **`/rtos-design`**: FreeRTOS görev öncelikleri, stack boyutu ve CPU yükü planlar.
- **`/pid-tune`**: Ziegler-Nichols yöntemiyle PID (Kp, Ki, Kd) katsayılarını hesaplar.
- **`/modbus-gen`**: Modbus RTU/TCP register haritası ve C struct başlık dosyası üretir.
- **`/mqtt-cfg`**: IoT MQTT topic hiyerarşisi ve QoS konfigürasyonu üretir.
- **`/print-cost`**: 3D baskı filament gramı, zaman ve elektrik maliyeti hesaplar.
- **`/motor-size`**: DC/BLDC/Stepper motor tork, RPM ve mekanik güç hesabı yapar.
- **`/bolt-torque`**: VDI 2230 standardında metrik cıvata sıkma torku ve ön gerilme force hesabı yapar.
- **`/rest-gen`**: FastAPI / Express CRUD REST API endpoint scaffold üretir.
- **`/ci-cd`**: GitHub Actions / GitLab CI otomatik test ve build YAML workflow üretir.
- **`/sql-gen`**: PostgreSQL / SQLite DDL tablo şeması ve index SQL scripti üretir.
- **`/health-probe`**: Sistem veritabanı, RAG store ve worker queue sağlık kontrolü yapar.

