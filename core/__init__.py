"""
Core Architectural Package Entrypoint.
Provides backward-compatible re-exports for all sub-packages:
- core.engine: Multi-Agent Pipeline, DAG Parallel Executor, Cost Router, Agent Telemetry, Critical Path & State Machine
- core.hardware: KiCad, SPICE, Pinout, Thermal, DRC, RF, Auto-Router, MCU Selector, Layer Stackup, KiCad 3D Models, SPICE Transpiler, DRC Rules, BOM Sensitivity, Footprint Crosscheck, Trace Length Matching, KiCad Subsheets, Solder Stencil & Genetic Optimizer
- core.software: Firmware, Unity Tests, Self-Healing, Edge AI, HIL Testing, Linter, Power Profiler, Static Security Scanner, Flash Partitions, OTA Verifier, Watchdog Analyzer, Test Coverage, Stack Guard & Bootloader Checker
- core.production: Mechanical CAD, BOM Optimizer, Harness Sizer, Report Generator, Presentation Exporter, FEA Simulation, BOM Stock Tracker, Screw Boss Fasteners, Airflow Calculator, Snap-Fit Joints, Flexure Hinges, Gasket Sizer & Cable Glands
- core.infra: RAG, Memory, Cache, Telemetry, Voice, Knowledge Graph, Guardrails, Plugins, Theme Manager, Autocomplete, Consensus Matrix, Pareto Frontier, Context Pruner, Circuit Breaker, Token Budget, Ensemble Aggregator, Memory Compactor, Adaptive Backoff, System Prompt Builder, Dead Letter Queue, Cost Forecast, Agent Health, Token Minimizer & DSPy Optimizer
"""

from core.engine.runner import run_agent_task
from core.engine.pipeline import AgentPipeline, embedded_dev_pipeline
from core.engine.layered_architecture import run_layered_pipeline
from core.engine.autonomous_agent import execute_autonomous_goal
from core.engine.agent_tree_sim import run_agent_tree_simulation, print_static_tree_topology
from core.engine.arena import run_agent_arena
from core.engine.dag_executor import global_dag_executor
from core.engine.cost_router import route_task_to_optimal_model
from core.engine.agent_telemetry import global_agent_telemetry
from core.engine.critical_path import calculate_critical_path
from core.engine.state_machine import global_agent_fsm

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
from core.hardware.layer_stackup import calculate_pcb_stackup
from core.hardware.kicad_3d_models import analyze_3d_component_clearance
from core.hardware.spice_transpiler import transpile_kicad_to_spice
from core.hardware.kicad_drc_rules import generate_kicad_dru_file
from core.hardware.bom_sensitivity import analyze_bom_cost_sensitivity
from core.hardware.footprint_crosscheck import crosscheck_footprint_pinout
from core.hardware.trace_length_matching import calculate_length_matching
from core.hardware.kicad_subsheets import generate_hierarchical_subsheets
from core.hardware.solder_stencil import calculate_solder_stencil_specs
from core.hardware.genetic_optimizer import run_genetic_hardware_optimization

from core.software.executor import execute_command, compile_c, compile_cpp
from core.software.self_heal import auto_compile_and_fix
from core.software.edge_ai import estimate_edge_ai_memory, generate_esp_dl_model_wrapper
from core.software.finetune import estimate_lora_vram, export_finetuning_dataset
from core.software.ota_builder import generate_ota_update_manifest
from core.software.embedded_test_gen import generate_unity_c_test
from core.software.hil_testing import run_hil_hardware_test
from core.software.linter import format_code_snippet
from core.software.power_profiler import profile_firmware_power
from core.software.static_analyzer import audit_firmware_security
from core.software.flash_partition import calculate_flash_partitions
from core.software.ota_verifier import verify_firmware_binary
from core.software.watchdog_analyzer import analyze_crash_dump
from core.software.test_coverage import generate_lcov_coverage_report
from core.software.stack_guard import analyze_task_stack_requirements
from core.software.bootloader_checker import audit_bootloader_config

from core.production.mechanical import generate_openscad_enclosure, recommend_slicer_settings
from core.production.battery import calculate_battery_lifespan
from core.production.bom_optimizer import optimize_bom_cost
from core.production.cart_builder import build_distributor_cart_payload
from core.production.gantt_planner import generate_project_gantt_chart
from core.production.harness import calculate_wire_harness
from core.production.project_gen import create_multidisciplinary_project
from core.production.report_generator import generate_project_markdown_report
from core.production.presentation_exporter import export_project_presentation
from core.production.fea_simulation import run_mechanical_fea_simulation
from core.production.bom_stock_tracker import check_bom_supply_chain_risks
from core.production.fasteners import calculate_screw_boss_dimensions
from core.production.airflow_calculator import calculate_enclosure_ventilation
from core.production.snap_fit import calculate_snap_fit_joint
from core.production.flexure_hinge import calculate_flexure_hinge
from core.production.gasket_sizer import calculate_gasket_groove_dimensions
from core.production.cable_gland import calculate_cable_gland_dimensions

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
from core.infra.consensus_matrix import calculate_consensus_matrix
from core.infra.pareto_frontier import calculate_pareto_frontier
from core.infra.context_pruner import compress_prompt_context
from core.infra.circuit_breaker import global_circuit_breaker
from core.infra.token_budget import global_token_budget
from core.infra.ensemble_aggregator import aggregate_ensemble_responses
from core.infra.memory_compactor import compact_agent_memory
from core.infra.adaptive_backoff import calculate_adaptive_backoff_delay
from core.infra.system_prompt_builder import build_personalized_engineer_prompt
from core.infra.dead_letter_queue import global_dlq
from core.infra.cost_forecast import forecast_token_costs
from core.infra.agent_health import get_system_subpackage_health
from core.infra.token_minimizer import count_and_estimate_tokens
from core.infra.dspy_optimizer import global_dspy_optimizer
