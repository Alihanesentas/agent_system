"""
Core Architectural Package Entrypoint.
Provides backward-compatible re-exports for all sub-packages:
- core.engine: Multi-Agent Pipeline, DAG Parallel Executor & Cost Router
- core.hardware: KiCad, SPICE, Pinout, Thermal, DRC, RF, Auto-Router & MCU Selector
- core.software: Firmware, Unity Tests, Self-Healing, Edge AI, HIL Testing & Linter
- core.production: Mechanical CAD, BOM Optimizer, Harness Sizer & Report Generator
- core.infra: RAG, Memory, Cache, Telemetry, Voice, Knowledge Graph, Guardrails, Plugins, Theme Manager & Autocomplete
"""

from core.engine.runner import run_agent_task
from core.engine.pipeline import AgentPipeline, embedded_dev_pipeline
from core.engine.layered_architecture import run_layered_pipeline
from core.engine.autonomous_agent import execute_autonomous_goal
from core.engine.agent_tree_sim import run_agent_tree_simulation, print_static_tree_topology
from core.engine.arena import run_agent_arena
from core.engine.dag_executor import global_dag_executor
from core.engine.cost_router import route_task_to_optimal_model

from core.hardware.schematics import parse_kicad_schematic, update_kicad_component_value
from core.hardware.datasheet import extract_datasheet
from core.hardware.component_search import search_component, get_component_alternatives, compare_components
from core.hardware.pinout import check_pinout_conflicts
from core.hardware.spice import simulate_rc_circuit, simulate_voltage_divider
from core.hardware.thermal import analyze_thermal_dissipation
from core.hardware.pcb_drc import calculate_trace_impedance, audit_pcb_drc_rules
from core.hardware.rf_antenna import calculate_rf_antenna_dimensions
from core.hardware.flasher import flash_firmware, read_serial_monitor
from core.hardware.emc_compliance import audit_emc_fcc_compliance
from core.hardware.vision import encode_image_to_base64
from core.hardware.autorouter import auto_route_pcb_netlist
from core.hardware.mcu_selector import recommend_mcu_for_project

from core.software.executor import execute_command, compile_c, compile_cpp
from core.software.self_heal import auto_compile_and_fix
from core.software.edge_ai import estimate_edge_ai_memory, generate_esp_dl_model_wrapper
from core.software.finetune import estimate_lora_vram, export_finetuning_dataset
from core.software.ota_builder import generate_ota_update_manifest
from core.software.embedded_test_gen import generate_unity_c_test
from core.software.hil_testing import run_hil_hardware_test
from core.software.linter import format_code_snippet

from core.production.mechanical import generate_openscad_enclosure, recommend_slicer_settings
from core.production.battery import calculate_battery_lifespan
from core.production.bom_optimizer import optimize_bom_cost
from core.production.cart_builder import build_distributor_cart_payload
from core.production.gantt_planner import generate_project_gantt_chart
from core.production.harness import calculate_wire_harness
from core.production.project_gen import create_multidisciplinary_project
from core.production.report_generator import generate_project_markdown_report

from core.infra.profile import load_user_profile, save_user_profile, build_personalized_system_prompt
from core.infra.cache import get_cache_metrics
from core.infra.telemetry import global_telemetry
from core.infra.rate_limiter import global_rate_limiter
from core.infra.worker_queue import global_worker_queue
from core.infra.checkpoint import create_system_checkpoint, restore_system_checkpoint
from core.infra.voice_agent import process_voice_command
from core.infra.knowledge_graph import global_knowledge_graph
from core.infra.self_reflection import run_with_self_reflection
from core.infra.guardrails import sanitize_and_verify_code
from core.infra.plugin_loader import discover_and_reload_plugins
from core.infra.theme_manager import set_cli_theme
