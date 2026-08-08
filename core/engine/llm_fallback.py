"""
LLM Fallback Script Generator & Executor Engine.
When no matching pre-built 0-token engine is found in ENGINE_REGISTRY,
this module allows the LLM to dynamically generate, validate, and execute
a Python script to handle the task — then optionally save it for future reuse.

Architecture:
  User Prompt → ENGINE_REGISTRY lookup → MISS → LLM generates Python → Sandbox Execute → Return Result
                                         HIT  → 0-token engine runs directly
"""

import os
import sys
import time
import json
import traceback
import hashlib
from typing import Dict, Any, Optional, List, Callable
from pathlib import Path

# ─── ENGINE REGISTRY ─────────────────────────────────────────────────────────
# Maps keywords/domains to existing 0-token Python engines.
# The autonomous agent searches this registry first before falling back to LLM generation.

ENGINE_REGISTRY: Dict[str, Dict[str, Any]] = {
    # ── Hardware & Electronics ──
    "pinout": {"module": "core.hardware.pinout", "func": "check_pinout_conflicts", "description": "ESP32 GPIO pin conflict & strapping pin audit"},
    "thermal": {"module": "core.hardware.thermal", "func": "analyze_thermal_dissipation", "description": "Thermal dissipation & heatsink sizing"},
    "trace_width": {"module": "core.hardware.pcb_drc", "func": "audit_pcb_drc_rules", "description": "PCB trace width & DRC audit"},
    "impedance": {"module": "core.hardware.pcb_drc", "func": "calculate_trace_impedance", "description": "Microstrip/stripline impedance calculation"},
    "mcu_select": {"module": "core.hardware.mcu_selector", "func": "recommend_mcu_for_project", "description": "MCU recommendation engine"},
    "stackup": {"module": "core.hardware.layer_stackup", "func": "calculate_pcb_stackup", "description": "PCB layer stackup calculator"},
    "spice": {"module": "core.hardware.spice", "func": "simulate_rc_circuit", "description": "SPICE RC circuit simulation"},
    "rf_antenna": {"module": "core.hardware.rf_antenna", "func": "calculate_rf_antenna_dimensions", "description": "RF antenna sizing"},
    "emc": {"module": "core.hardware.emc_compliance", "func": "audit_emc_fcc_compliance", "description": "EMC/FCC compliance audit"},
    "autoroute": {"module": "core.hardware.autorouter", "func": "auto_route_pcb_netlist", "description": "PCB auto-routing"},
    "stencil": {"module": "core.hardware.solder_stencil", "func": "calculate_solder_stencil_specs", "description": "Solder paste stencil calculator"},
    "trace_matching": {"module": "core.hardware.trace_length_matching", "func": "calculate_length_matching", "description": "Differential pair length matching"},
    "3d_clearance": {"module": "core.hardware.kicad_3d_models", "func": "analyze_3d_component_clearance", "description": "3D component height clearance audit"},
    "footprint": {"module": "core.hardware.footprint_crosscheck", "func": "crosscheck_footprint_pinout", "description": "Symbol vs footprint cross-check"},
    "bom_sensitivity": {"module": "core.hardware.bom_sensitivity", "func": "analyze_bom_cost_sensitivity", "description": "Monte Carlo BOM cost sensitivity"},
    "genetic_hw": {"module": "core.hardware.genetic_optimizer", "func": "run_genetic_hardware_optimization", "description": "Genetic hardware optimization"},
    "subsheets": {"module": "core.hardware.kicad_subsheets", "func": "generate_hierarchical_subsheets", "description": "KiCad hierarchical subsheet generator"},
    "drc_rules": {"module": "core.hardware.kicad_drc_rules", "func": "generate_kicad_dru_file", "description": "KiCad DRC rules exporter"},
    "smps": {"module": "core.hardware.smps_design", "func": "design_smps_converter", "description": "Buck/Boost SMPS converter design"},
    "power_budget": {"module": "core.hardware.power_budget", "func": "calculate_power_budget", "description": "System power budget calculator"},
    "voltage_divider": {"module": "core.hardware.voltage_divider", "func": "calculate_voltage_divider", "description": "Resistor voltage divider calculator"},
    "i2c_pullup": {"module": "core.hardware.i2c_pullup", "func": "calculate_i2c_pullup", "description": "I2C bus pull-up resistor calculator"},
    "esd": {"module": "core.hardware.esd_protection", "func": "design_esd_protection", "description": "ESD protection TVS diode sizer"},
    "opamp": {"module": "core.hardware.opamp_circuit", "func": "calculate_opamp_circuit", "description": "Op-Amp gain & bandwidth calculator"},
    "adc_snr": {"module": "core.hardware.adc_snr", "func": "analyze_adc_performance", "description": "ADC SNR & ENOB performance analyzer"},
    "can_bus": {"module": "core.hardware.can_bus", "func": "configure_can_bus", "description": "CAN bus bit timing & termination calculator"},
    "via_current": {"module": "core.hardware.via_current", "func": "calculate_via_current", "description": "PCB via current capacity & thermal array calculator"},
    "ldo_thermal": {"module": "core.hardware.ldo_thermal", "func": "analyze_ldo_thermal", "description": "LDO regulator thermal & dropout analyzer"},
    "mosfet_driver": {"module": "core.hardware.mosfet_driver", "func": "design_mosfet_driver", "description": "High/Low-side MOSFET gate driver & switching loss sizer"},
    "analog_filter": {"module": "core.hardware.filter_design", "func": "design_analog_filter", "description": "Active & passive analog Sallen-Key filter designer"},
    "current_sense": {"module": "core.hardware.current_sense", "func": "design_current_sense", "description": "Shunt resistor & INA current sense circuit designer"},
    "uart_config": {"module": "core.hardware.uart_config", "func": "configure_uart", "description": "UART baud rate, clock divider & error % calculator"},
    "wheatstone_bridge": {"module": "core.hardware.wheatstone_bridge", "func": "calculate_wheatstone_bridge", "description": "Wheatstone bridge & strain gauge load cell calculator"},
    "pcb_cost": {"module": "core.hardware.pcb_cost_estimator", "func": "estimate_pcb_cost", "description": "PCB fabrication & SMT assembly cost estimator"},
    
    # ── Software & Firmware ──
    "bootloader": {"module": "core.software.bootloader_checker", "func": "audit_bootloader_config", "description": "Bootloader integrity checker"},
    "stack_guard": {"module": "core.software.stack_guard", "func": "analyze_task_stack_requirements", "description": "FreeRTOS stack guard analyzer"},
    "power_profile": {"module": "core.software.power_profiler", "func": "profile_firmware_power", "description": "Firmware power profiler"},
    "flash_partition": {"module": "core.software.flash_partition", "func": "calculate_flash_partitions", "description": "Flash partition table layout"},
    "ota": {"module": "core.software.ota_builder", "func": "generate_ota_update_manifest", "description": "OTA update manifest builder"},
    "watchdog": {"module": "core.software.watchdog_analyzer", "func": "analyze_crash_dump", "description": "Crash dump & watchdog analyzer"},
    "security_audit": {"module": "core.software.static_analyzer", "func": "audit_firmware_security", "description": "Firmware security static analysis"},
    "coverage": {"module": "core.software.test_coverage", "func": "generate_lcov_coverage_report", "description": "LCOV test coverage reporter"},
    "edge_ai": {"module": "core.software.edge_ai", "func": "estimate_edge_ai_memory", "description": "TinyML memory estimator"},
    "hil_test": {"module": "core.software.hil_testing", "func": "run_hil_hardware_test", "description": "Hardware-in-the-loop testing"},
    "unittest_gen": {"module": "core.software.embedded_test_gen", "func": "generate_unity_c_test", "description": "Unity C test generator"},
    "rtos_design": {"module": "core.software.rtos_task_design", "func": "design_rtos_tasks", "description": "FreeRTOS task priority & stack designer"},
    "pid_tuner": {"module": "core.software.pid_tuner", "func": "tune_pid_controller", "description": "PID controller auto-tuner"},
    "modbus": {"module": "core.software.modbus_gen", "func": "generate_modbus_map", "description": "Modbus register map & C struct generator"},
    "mqtt": {"module": "core.software.mqtt_topic", "func": "generate_mqtt_config", "description": "MQTT topic hierarchy & QoS generator"},
    "ble_gatt": {"module": "core.software.ble_gatt", "func": "generate_ble_gatt_profile", "description": "BLE GATT service profile & C code generator"},
    "lorawan": {"module": "core.software.lorawan_params", "func": "calculate_lorawan_params", "description": "LoRaWAN airtime & link budget calculator"},
    "crypto": {"module": "core.software.crypto_engine", "func": "design_crypto_params", "description": "Crypto hardware accelerator throughput & key sizer"},
    "digital_filter": {"module": "core.software.fir_iir_filter", "func": "design_digital_filter", "description": "FIR/IIR digital filter tap coefficient generator"},
    "isr_latency": {"module": "core.software.isr_latency", "func": "analyze_isr_latency", "description": "ISR latency & nested interrupt analyzer"},
    "memory_pool": {"module": "core.software.memory_pool", "func": "design_memory_pool", "description": "Static fixed-block embedded memory pool designer"},
    "ring_buffer": {"module": "core.software.ring_buffer", "func": "design_ring_buffer", "description": "Lock-free circular ring buffer sizer & C code generator"},
    
    # ── Production & Mechanical ──
    "enclosure": {"module": "core.production.mechanical", "func": "generate_openscad_enclosure", "description": "3D enclosure generator"},
    "snap_fit": {"module": "core.production.snap_fit", "func": "calculate_snap_fit_joint", "description": "Snap-fit joint calculator"},
    "flexure": {"module": "core.production.flexure_hinge", "func": "calculate_flexure_hinge", "description": "Living hinge calculator"},
    "gasket": {"module": "core.production.gasket_sizer", "func": "calculate_gasket_groove_dimensions", "description": "IP67 gasket sizer"},
    "cable_gland": {"module": "core.production.cable_gland", "func": "calculate_cable_gland_dimensions", "description": "Cable gland sizer"},
    "fasteners": {"module": "core.production.fasteners", "func": "calculate_screw_boss_dimensions", "description": "Screw boss sizer"},
    "fea": {"module": "core.production.fea_simulation", "func": "run_mechanical_fea_simulation", "description": "Mechanical FEA stress simulation"},
    "airflow": {"module": "core.production.airflow_calculator", "func": "calculate_enclosure_ventilation", "description": "Enclosure ventilation calculator"},
    "battery": {"module": "core.production.battery", "func": "calculate_battery_lifespan", "description": "Battery lifespan calculator"},
    "harness": {"module": "core.production.harness", "func": "calculate_wire_harness", "description": "Wire harness AWG sizer"},
    "bom_opt": {"module": "core.production.bom_optimizer", "func": "optimize_bom_cost", "description": "BOM cost optimizer"},
    "gantt": {"module": "core.production.gantt_planner", "func": "generate_project_gantt_chart", "description": "Project Gantt chart"},
    "print_cost": {"module": "core.production.print_cost", "func": "estimate_3d_print_cost", "description": "3D print manufacturing cost estimator"},
    "motor_size": {"module": "core.production.motor_sizing", "func": "size_motor", "description": "Motor torque & power sizer"},
    "bolt_torque": {"module": "core.production.bolt_torque", "func": "calculate_bolt_torque", "description": "Bolt tightening torque calculator"},
    "spring_design": {"module": "core.production.spring_design", "func": "design_spring", "description": "Helical compression spring design engine"},
    "gear_ratio": {"module": "core.production.gear_ratio", "func": "calculate_gear_ratio", "description": "Gear train ratio & backlash calculator"},
    "heatsink": {"module": "core.production.heatsink_design", "func": "design_heatsink", "description": "Aluminum finned heatsink dimensioning engine"},
    "tolerance_stack": {"module": "core.production.tolerance_stack", "func": "analyze_tolerance_stack", "description": "Tolerance stack-up analysis engine (Worst-Case & RSS)"},
    "bearing_life": {"module": "core.production.bearing_life", "func": "calculate_bearing_life", "description": "ISO 281 ball & roller bearing L10 life calculator"},
    
    # ── Infrastructure ──
    "cost_forecast": {"module": "core.infra.cost_forecast", "func": "forecast_token_costs", "description": "Token cost forecast"},
    "token_count": {"module": "core.infra.token_minimizer", "func": "count_and_estimate_tokens", "description": "BPE token counter"},
    "agent_health": {"module": "core.infra.agent_health", "func": "get_system_subpackage_health", "description": "System health monitor"},
    "dlq": {"module": "core.infra.dead_letter_queue", "func": "global_dlq", "description": "Dead letter queue"},
    "critical_path": {"module": "core.engine.critical_path", "func": "calculate_critical_path", "description": "Critical path profiler"},
    "prompt_template": {"module": "core.engine.prompt_template", "func": "render_prompt_template", "description": "Versioned prompt template renderer"},
    "chain_of_thought": {"module": "core.engine.chain_of_thought", "func": "run_chain_of_thought", "description": "Chain-of-thought reasoning framework"},
    "health_check": {"module": "core.infra.health_check", "func": "run_health_check", "description": "Service health probe runner"},
    "cron_scheduler": {"module": "core.infra.cron_scheduler", "func": "schedule_cron_job", "description": "Background cron task scheduler"},
    "env_manager": {"module": "core.infra.env_manager", "func": "manage_env_config", "description": "Environment variable & secret key manager (.env)"},
    
    # ── Computer / Web ──
    "web_api": {"module": "core.computer.web_stack", "func": "generate_web_api_architecture", "description": "REST API scaffold generator"},
    "microservice": {"module": "core.computer.microservices", "func": "generate_microservice_proto", "description": "gRPC proto generator"},
    "react": {"module": "core.computer.frontend_gen", "func": "generate_react_component", "description": "React component generator"},
    "complexity": {"module": "core.computer.code_complexity", "func": "audit_code_complexity", "description": "Code complexity auditor"},
    "rest_gen": {"module": "core.computer.rest_api_gen", "func": "generate_rest_api_scaffold", "description": "REST API router scaffold generator"},
    "ci_cd": {"module": "core.computer.ci_cd_pipeline", "func": "generate_ci_cd_pipeline", "description": "CI/CD workflow pipeline generator"},
    "sql_gen": {"module": "core.computer.sql_schema_gen", "func": "generate_sql_schema", "description": "SQL DDL schema generator"},
    "graphql_gen": {"module": "core.computer.graphql_schema", "func": "generate_graphql_schema", "description": "GraphQL SDL schema & resolver generator"},
    "terraform_gen": {"module": "core.computer.terraform_gen", "func": "generate_terraform_module", "description": "Terraform IaC module generator"},
    "auth_flow": {"module": "core.computer.auth_flow", "func": "generate_auth_flow", "description": "OAuth2, JWT & API key authentication strategy generator"},
    "nginx_gen": {"module": "core.computer.nginx_config", "func": "generate_nginx_config", "description": "Nginx reverse proxy, SSL & rate limit config generator"},
}

# ─── KEYWORD ALIASES ─────────────────────────────────────────────────────────
# Maps natural language keywords to ENGINE_REGISTRY keys for fuzzy matching
KEYWORD_ALIASES: Dict[str, List[str]] = {
    "pinout": ["pin", "gpio", "strapping", "pin conflict", "pin mapping"],
    "thermal": ["heat", "temperature", "thermal", "heatsink", "soğutucu", "ısı", "sıcaklık"],
    "trace_width": ["trace", "pcb trace", "copper width", "drc"],
    "impedance": ["impedance", "impedans", "ohm", "microstrip", "stripline"],
    "mcu_select": ["mcu", "microcontroller", "esp32", "stm32", "rp2040", "nrf52", "mikrodenetleyici"],
    "stackup": ["stackup", "layer", "katman", "fr4", "dielectric"],
    "spice": ["spice", "simulation", "rc circuit", "frequency response", "simülasyon"],
    "rf_antenna": ["antenna", "rf", "anten", "wireless", "bluetooth", "wifi"],
    "emc": ["emc", "fcc", "ce", "electromagnetic", "emi", "radiated emission"],
    "stencil": ["stencil", "solder paste", "lehim", "smd", "reflow"],
    "smps": ["smps", "buck", "boost", "converter", "dcdc", "power supply"],
    "power_budget": ["power budget", "current draw", "power consumption", "güç bütçesi"],
    "voltage_divider": ["voltage divider", "resistor divider", "voltaj bölücü"],
    "i2c_pullup": ["i2c pullup", "i2c pull-up", "pullup resistor", "bus capacitance"],
    "esd": ["esd", "tvs", "surge", "transient", "diode"],
    "opamp": ["opamp", "op-amp", "operational amplifier", "amplifikatör"],
    "adc_snr": ["adc", "snr", "enob", "quantization noise"],
    "can_bus": ["can bus", "canbus", "can fd", "bit timing"],
    "via_current": ["via", "via current", "thermal via", "ipc-2152"],
    "ldo_thermal": ["ldo", "dropout", "quiescent current", "regülatör"],
    "mosfet_driver": ["mosfet", "gate driver", "gate charge", "switching loss"],
    "analog_filter": ["analog filter", "sallen key", "butterworth filter"],
    "current_sense": ["current sense", "shunt", "ina219", "ina180"],
    "uart_config": ["uart", "baud rate", "parity", "usart"],
    "wheatstone_bridge": ["wheatstone", "strain gauge", "load cell", "köprü"],
    "pcb_cost": ["pcb cost", "pcb manufacturing cost", "smt cost"],
    "bootloader": ["bootloader", "boot", "vector table", "flash offset"],
    "stack_guard": ["stack", "freertos", "rtos task", "stack overflow"],
    "power_profile": ["power", "current", "sleep", "deep sleep", "mA", "güç", "batarya ömrü"],
    "flash_partition": ["partition", "nvs", "ota partition", "flash layout"],
    "ota": ["ota", "update", "firmware update", "güncelleme"],
    "rtos_design": ["rtos design", "freertos task", "task priority", "rtos stack"],
    "pid_tuner": ["pid", "pid tuner", "ziegler nichols", "kp ki kd"],
    "modbus": ["modbus", "modbus rtu", "modbus tcp", "holding register"],
    "mqtt": ["mqtt", "mqtt topic", "qos", "broker"],
    "ble_gatt": ["ble", "gatt", "bluetooth", "uuid", "characteristic"],
    "lorawan": ["lorawan", "lora", "spreading factor", "time on air"],
    "crypto": ["crypto", "aes", "ecc", "sha256", "hardware accelerator"],
    "digital_filter": ["fir", "iir", "digital filter", "filter taps"],
    "isr_latency": ["isr", "interrupt latency", "nvic", "wcet"],
    "memory_pool": ["memory pool", "static memory", "fixed block"],
    "ring_buffer": ["ring buffer", "circular buffer", "dma buffer", "lock free"],
    "enclosure": ["enclosure", "box", "case", "kutu", "3d print", "openscad"],
    "snap_fit": ["snap", "clip", "klips", "cantilever"],
    "gasket": ["gasket", "o-ring", "seal", "conta", "ip67", "waterproof", "su geçirmez"],
    "cable_gland": ["cable gland", "kablo rakoru", "pg7", "pg9", "m12"],
    "battery": ["battery", "batarya", "pil", "solar", "güneş paneli"],
    "fea": ["fea", "stress", "strain", "gerilme", "deformasyon", "von mises"],
    "harness": ["wire", "harness", "awg", "kablo", "iletken"],
    "print_cost": ["print cost", "3d print cost", "filament cost", "baskı maliyeti"],
    "motor_size": ["motor size", "motor sizing", "torque", "motor torku"],
    "bolt_torque": ["bolt torque", "tightening torque", "civata torku"],
    "spring_design": ["spring", "spring rate", "helical spring", "yay hesabı"],
    "gear_ratio": ["gear", "gear ratio", "dişli oranı", "gearbox"],
    "heatsink": ["heatsink", "thermal resistance", "soğutucu kanatçık"],
    "tolerance_stack": ["tolerance stack", "tolerance analysis", "worst case", "rss"],
    "bearing_life": ["bearing", "bearing life", "l10", "rulman ömrü"],
    "web_api": ["api", "rest", "fastapi", "express", "backend"],
    "react": ["react", "frontend", "component", "tsx", "jsx"],
    "edge_ai": ["tinyml", "edge ai", "model deploy", "quantization"],
    "ci_cd": ["ci cd", "github actions", "pipeline", "workflow"],
    "sql_gen": ["sql", "ddl", "postgres", "table schema"],
    "graphql_gen": ["graphql", "sdl", "resolver", "query mutation"],
    "terraform_gen": ["terraform", "iac", "hcl", "aws infrastructure"],
    "auth_flow": ["auth", "jwt", "oauth2", "authentication"],
    "nginx_gen": ["nginx", "reverse proxy", "ssl", "tls"],
    "env_manager": ["env", "environment variables", "secret key", "secret rotation"],
    "cost_forecast": ["cost", "maliyet", "token cost", "api cost"],
    "agent_health": ["health", "sağlık", "system status", "sistem durumu"],
}




# ─── GENERATED SCRIPTS CACHE ─────────────────────────────────────────────────
# Directory where dynamically generated scripts are saved for reuse
GENERATED_SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "generated_engines")


def _ensure_generated_dir():
    """Ensures the generated_engines directory exists."""
    os.makedirs(GENERATED_SCRIPTS_DIR, exist_ok=True)


def _hash_task(task_description: str) -> str:
    """Creates a deterministic hash for a task description."""
    return hashlib.md5(task_description.lower().strip().encode()).hexdigest()[:12]


# ─── REGISTRY SEARCH ─────────────────────────────────────────────────────────

def search_engine_registry(user_prompt: str) -> Optional[Dict[str, Any]]:
    """
    Searches the ENGINE_REGISTRY for a matching 0-token engine.
    Uses keyword alias matching for fuzzy natural language lookups.
    Uses word-boundary aware matching to prevent false positives.
    
    Returns:
        Matching engine entry dict if found, None if no match (triggers LLM fallback).
    """
    prompt_lower = user_prompt.lower()
    prompt_words = set(prompt_lower.split())
    
    # 1. Direct key match (exact word boundary)
    for key, engine in ENGINE_REGISTRY.items():
        if key in prompt_words or key.replace("_", " ") in prompt_lower:
            return {"matched_key": key, **engine}
    
    # 2. Keyword alias fuzzy match (word boundary aware)
    for key, aliases in KEYWORD_ALIASES.items():
        for alias in aliases:
            # For single-word aliases, check word boundary
            if " " not in alias:
                if alias in prompt_words:
                    if key in ENGINE_REGISTRY:
                        return {"matched_key": key, **ENGINE_REGISTRY[key]}
            else:
                # For multi-word aliases, check substring
                if alias in prompt_lower:
                    if key in ENGINE_REGISTRY:
                        return {"matched_key": key, **ENGINE_REGISTRY[key]}
    
    # 3. No match — LLM fallback will be triggered
    return None



def load_engine_dynamically(module_path: str, func_name: str) -> Optional[Callable]:
    """
    Dynamically imports a module and returns the target function.
    Used to lazily load engines only when needed.
    """
    try:
        import importlib
        mod = importlib.import_module(module_path)
        return getattr(mod, func_name)
    except (ImportError, AttributeError) as e:
        return None


# ─── LLM FALLBACK SCRIPT GENERATOR ──────────────────────────────────────────

def generate_fallback_script(task_description: str, llm_client_func=None) -> Dict[str, Any]:
    """
    When no matching pre-built engine is found, this function:
    1. Asks the LLM to generate a purpose-built Python script
    2. Validates the generated code for safety
    3. Executes it in a restricted sandbox
    4. Returns the result
    5. Optionally saves the script for future reuse
    
    Args:
        task_description: The user's natural language task
        llm_client_func: Optional callable that takes a prompt and returns generated code.
                         If None, returns a template for manual LLM generation.
    
    Returns:
        Dict with status, generated_code, execution_result, and saved_path
    """
    _ensure_generated_dir()
    task_hash = _hash_task(task_description)
    
    # Check if we already generated & cached a script for this exact task
    cached_path = os.path.join(GENERATED_SCRIPTS_DIR, f"gen_{task_hash}.py")
    if os.path.exists(cached_path):
        return _execute_cached_script(cached_path, task_description)
    
    # Build the LLM prompt for code generation
    generation_prompt = _build_generation_prompt(task_description)
    
    if llm_client_func is not None:
        # LLM generates the code
        generated_code = llm_client_func(generation_prompt)
    else:
        # Return the prompt template for external LLM to handle
        return {
            "status": "llm_generation_required",
            "task_description": task_description,
            "generation_prompt": generation_prompt,
            "instruction": "Pass this prompt to your LLM client to generate the script, then call execute_generated_script() with the result."
        }
    
    # Validate the generated code
    validation = _validate_generated_code(generated_code)
    if not validation["safe"]:
        return {
            "status": "rejected",
            "reason": validation["reason"],
            "task_description": task_description
        }
    
    # Execute in sandbox
    result = _sandbox_execute(generated_code, task_description)
    
    # Cache the script if execution was successful
    if result["status"] == "success":
        _save_generated_script(cached_path, generated_code, task_description)
    
    return result


def _build_generation_prompt(task_description: str) -> str:
    """Builds the system prompt that instructs the LLM how to generate the script."""
    return f"""You are a Python script generator for an engineering agent system.
Generate a SINGLE self-contained Python function that accomplishes this task:

TASK: {task_description}

RULES:
1. The function MUST be named `execute_task`
2. The function MUST accept **kwargs and return Dict[str, Any]
3. The function MUST have a 'status' key in the return dict ('success' or 'error')
4. Use ONLY Python standard library (math, json, os, datetime, collections, itertools, statistics, etc.)
5. Do NOT use subprocess, eval, exec, __import__, compile, or any code execution functions
6. Do NOT use network calls (requests, urllib, socket, http)
7. Do NOT use file system writes (open with 'w', os.remove, shutil.rmtree)
8. Include a descriptive docstring
9. Include realistic calculations with proper engineering formulas
10. Return structured data with clear keys and units

EXAMPLE OUTPUT FORMAT:
```python
import math
from typing import Dict, Any

def execute_task(**kwargs) -> Dict[str, Any]:
    \"\"\"Calculates [description].\"\"\"
    # ... calculations ...
    return {{
        "status": "success",
        "result_name": calculated_value,
        "unit": "mm"
    }}
```

Generate ONLY the Python code, no explanations."""


def _validate_generated_code(code: str) -> Dict[str, Any]:
    """
    Validates generated code for safety before execution.
    Blocks dangerous operations.
    """
    BLOCKED_PATTERNS = [
        "subprocess", "os.system", "os.popen", "os.exec",
        "eval(", "exec(", "compile(", "__import__(",
        "open(", "shutil.rmtree", "os.remove", "os.unlink",
        "requests.", "urllib.", "http.client", "socket.",
        "pickle.", "marshal.", "ctypes.",
        "sys.exit", "os._exit", "os.kill",
        "globals()", "locals()", "vars()",
    ]
    
    for pattern in BLOCKED_PATTERNS:
        if pattern in code:
            return {"safe": False, "reason": f"Blocked pattern detected: '{pattern}'"}
    
    # Check that execute_task function exists
    if "def execute_task" not in code:
        return {"safe": False, "reason": "Missing required 'execute_task' function"}
    
    # Check code length (prevent excessively large scripts)
    if len(code) > 50000:
        return {"safe": False, "reason": "Generated code exceeds 50KB safety limit"}
    
    return {"safe": True, "reason": "All safety checks passed"}


def _sandbox_execute(code: str, task_description: str) -> Dict[str, Any]:
    """
    Executes generated code in a restricted namespace sandbox.
    Only allows safe standard library imports.
    """
    ALLOWED_MODULES = {
        "math": __import__("math"),
        "json": __import__("json"),
        "datetime": __import__("datetime"),
        "collections": __import__("collections"),
        "itertools": __import__("itertools"),
        "statistics": __import__("statistics"),
        "re": __import__("re"),
        "decimal": __import__("decimal"),
        "fractions": __import__("fractions"),
        "random": __import__("random"),
        "string": __import__("string"),
        "textwrap": __import__("textwrap"),
        "copy": __import__("copy"),
        "functools": __import__("functools"),
        "operator": __import__("operator"),
        "typing": __import__("typing"),
    }
    
    # Build restricted global namespace
    sandbox_globals = {
        "__builtins__": {
            # Safe builtins only
            "abs": abs, "all": all, "any": any, "bin": bin,
            "bool": bool, "chr": chr, "dict": dict, "divmod": divmod,
            "enumerate": enumerate, "filter": filter, "float": float,
            "format": format, "frozenset": frozenset, "hex": hex,
            "int": int, "isinstance": isinstance, "issubclass": issubclass,
            "iter": iter, "len": len, "list": list, "map": map,
            "max": max, "min": min, "next": next, "oct": oct,
            "ord": ord, "pow": pow, "print": print, "range": range,
            "repr": repr, "reversed": reversed, "round": round,
            "set": set, "slice": slice, "sorted": sorted, "str": str,
            "sum": sum, "tuple": tuple, "type": type, "zip": zip,
            "True": True, "False": False, "None": None,
            "ValueError": ValueError, "TypeError": TypeError,
            "KeyError": KeyError, "IndexError": IndexError,
            "ZeroDivisionError": ZeroDivisionError,
            "Exception": Exception,
            "Dict": dict, "Any": object, "List": list, "Optional": None,
        },
    }
    
    # Inject allowed modules
    for mod_name, mod in ALLOWED_MODULES.items():
        sandbox_globals[mod_name] = mod
    
    try:
        # Compile and execute in sandbox
        compiled = compile(code, "<llm_generated>", "exec")
        exec(compiled, sandbox_globals)
        
        # Call the execute_task function
        if "execute_task" not in sandbox_globals:
            return {"status": "error", "error": "execute_task function not found after compilation"}
        
        execute_fn = sandbox_globals["execute_task"]
        result = execute_fn(task=task_description)
        
        if not isinstance(result, dict):
            result = {"status": "success", "raw_output": str(result)}
        
        result["_meta"] = {
            "source": "llm_fallback_generated",
            "code_length_bytes": len(code),
            "task_description": task_description
        }
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "task_description": task_description,
            "_meta": {"source": "llm_fallback_generated", "execution_failed": True}
        }


def _execute_cached_script(cached_path: str, task_description: str) -> Dict[str, Any]:
    """Executes a previously generated and cached script."""
    try:
        with open(cached_path, "r", encoding="utf-8") as f:
            code = f.read()
        result = _sandbox_execute(code, task_description)
        result["_meta"] = result.get("_meta", {})
        result["_meta"]["cached"] = True
        result["_meta"]["cached_path"] = cached_path
        return result
    except Exception as e:
        return {"status": "error", "error": f"Cache execution failed: {str(e)}"}


def _save_generated_script(path: str, code: str, task_description: str):
    """Saves generated script to disk for future reuse."""
    header = f'# Auto-generated by LLM Fallback Engine\n# Task: {task_description}\n# Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}\n\n'
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(header + code)
    except Exception:
        pass  # Non-critical — script still ran successfully


def execute_generated_script(code: str, task_description: str) -> Dict[str, Any]:
    """
    Public API for executing LLM-generated code.
    Call this after your LLM client generates the script.
    
    Args:
        code: The Python source code generated by the LLM
        task_description: Original task description
    
    Returns:
        Execution result dict
    """
    validation = _validate_generated_code(code)
    if not validation["safe"]:
        return {"status": "rejected", "reason": validation["reason"]}
    
    result = _sandbox_execute(code, task_description)
    
    if result["status"] == "success":
        _ensure_generated_dir()
        task_hash = _hash_task(task_description)
        cached_path = os.path.join(GENERATED_SCRIPTS_DIR, f"gen_{task_hash}.py")
        _save_generated_script(cached_path, code, task_description)
    
    return result


# ─── UNIFIED DISPATCH ────────────────────────────────────────────────────────

def smart_dispatch(user_prompt: str, llm_client_func=None) -> Dict[str, Any]:
    """
    The main entry point for the intelligent dispatch system.
    
    Flow:
    1. Search ENGINE_REGISTRY for a matching 0-token engine
    2. If found → execute locally (0 tokens, instant)
    3. If not found → LLM generates a script on-the-fly → sandbox execute
    
    Args:
        user_prompt: Natural language task from the user
        llm_client_func: Optional LLM client callable for code generation
    
    Returns:
        Execution result dict with source metadata
    """
    start_time = time.time()
    
    # Step 1: Try ENGINE_REGISTRY (0-token path)
    match = search_engine_registry(user_prompt)
    
    if match:
        # Found a pre-built engine — execute with 0 tokens
        engine_func = load_engine_dynamically(match["module"], match["func"])
        if engine_func:
            try:
                result = engine_func()  # Default params — the autonomous agent handles proper params
                if not isinstance(result, dict):
                    result = {"status": "success", "output": str(result)}
                result["_dispatch"] = {
                    "source": "engine_registry",
                    "matched_key": match["matched_key"],
                    "engine": match["description"],
                    "tokens_used": 0,
                    "cost_usd": 0.0,
                    "latency_ms": round((time.time() - start_time) * 1000, 2)
                }
                return result
            except Exception as e:
                # Engine exists but failed — fall through to LLM
                pass
    
    # Step 2: No match or engine failed — LLM fallback
    result = generate_fallback_script(user_prompt, llm_client_func)
    result["_dispatch"] = {
        "source": "llm_fallback",
        "matched_key": None,
        "engine": "LLM-Generated Script",
        "tokens_used": "varies",
        "cost_usd": "varies",
        "latency_ms": round((time.time() - start_time) * 1000, 2)
    }
    return result


def list_all_engines() -> Dict[str, Any]:
    """Lists all registered engines and their descriptions."""
    return {
        "total_engines": len(ENGINE_REGISTRY),
        "engines": {
            key: {
                "module": val["module"],
                "function": val["func"],
                "description": val["description"]
            }
            for key, val in ENGINE_REGISTRY.items()
        },
        "fallback": "LLM Script Generator (generates & caches scripts on-the-fly)"
    }


def get_generated_scripts_list() -> Dict[str, Any]:
    """Lists all cached generated scripts."""
    _ensure_generated_dir()
    scripts = []
    for f in os.listdir(GENERATED_SCRIPTS_DIR):
        if f.endswith(".py"):
            fpath = os.path.join(GENERATED_SCRIPTS_DIR, f)
            # Read first 3 lines to get task description
            try:
                with open(fpath, "r") as fh:
                    lines = fh.readlines()[:3]
                    task_line = [l for l in lines if l.startswith("# Task:")]
                    task = task_line[0].replace("# Task:", "").strip() if task_line else "Unknown"
            except Exception:
                task = "Unknown"
            scripts.append({"file": f, "task": task, "path": fpath})
    
    return {
        "total_cached_scripts": len(scripts),
        "scripts": scripts,
        "cache_directory": GENERATED_SCRIPTS_DIR
    }
