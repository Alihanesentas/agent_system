"""
Core Architectural Package Entrypoint.
Provides backward-compatible re-exports for all 6 sub-packages:
- core.engine: Multi-Agent Pipeline, DAG Parallel Executor, Cost Router, Agent Telemetry, Critical Path & State Machine
- core.hardware: KiCad, SPICE, Pinout, Thermal, DRC, RF, Auto-Router, MCU Selector, Layer Stackup, KiCad 3D Models, SPICE Transpiler, DRC Rules, BOM Sensitivity, Footprint Crosscheck, Trace Length Matching, KiCad Subsheets, Solder Stencil & Genetic Optimizer
- core.software: Firmware, Unity Tests, Self-Healing, Edge AI, HIL Testing, Linter, Power Profiler, Static Security Scanner, Flash Partitions, OTA Verifier, Watchdog Analyzer, Test Coverage, Stack Guard, Bootloader Checker, Docker/K8s Generator, UML Generator, DB Migration & DevOps Terraform
- core.computer: Full-Stack Web REST APIs, gRPC Microservices, React TSX Frontend, Cyclomatic Code Complexity Auditor
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
from core.hardware.smps_design import design_smps_converter
from core.hardware.power_budget import calculate_power_budget
from core.hardware.voltage_divider import calculate_voltage_divider
from core.hardware.i2c_pullup import calculate_i2c_pullup
from core.hardware.esd_protection import design_esd_protection
from core.hardware.opamp_circuit import calculate_opamp_circuit
from core.hardware.adc_snr import analyze_adc_performance
from core.hardware.can_bus import configure_can_bus
from core.hardware.via_current import calculate_via_current
from core.hardware.ldo_thermal import analyze_ldo_thermal
from core.hardware.mosfet_driver import design_mosfet_driver
from core.hardware.filter_design import design_analog_filter
from core.hardware.current_sense import design_current_sense
from core.hardware.uart_config import configure_uart
from core.hardware.wheatstone_bridge import calculate_wheatstone_bridge
from core.hardware.pcb_cost_estimator import estimate_pcb_cost
from core.hardware.psu_ripple import analyze_psu_ripple
from core.hardware.spi_timing import analyze_spi_timing
from core.hardware.usb_impedance import check_usb_impedance
from core.hardware.fuse_sizing import calculate_fuse_sizing
from core.hardware.reverse_polarity import design_reverse_polarity_protection
from core.hardware.dac_output import design_dac_output
from core.hardware.ethernet_magnetics import design_ethernet_interface
from core.hardware.lvds_serdes import analyze_lvds_signal
from core.hardware.sensor_interface import design_sensor_interface
from core.hardware.thermocouple import design_thermocouple_interface
from core.hardware.crosstalk_analysis import analyze_pcb_crosstalk
from core.hardware.impedance_calculator import calculate_trace_impedance_advanced
from core.hardware.panelization import optimize_pcb_panel
from core.hardware.gerber_checker import validate_gerber_files
from core.hardware.pcb_thermal_relief import calculate_thermal_relief

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
from core.software.docker_k8s import generate_docker_k8s_manifests
from core.software.uml_generator import generate_uml_architecture_diagram
from core.software.db_migration import generate_db_schema_and_migrations
from core.software.cloud_devops import generate_devops_terraform_config
from core.software.rtos_task_design import design_rtos_tasks
from core.software.pid_tuner import tune_pid_controller
from core.software.modbus_gen import generate_modbus_map
from core.software.mqtt_topic import generate_mqtt_config
from core.software.ble_gatt import generate_ble_gatt_profile
from core.software.lorawan_params import calculate_lorawan_params
from core.software.crypto_engine import design_crypto_params
from core.software.fir_iir_filter import design_digital_filter
from core.software.isr_latency import analyze_isr_latency
from core.software.memory_pool import design_memory_pool
from core.software.ring_buffer import design_ring_buffer
from core.software.mutex_deadlock import detect_mutex_deadlock
from core.software.protobuf_gen import generate_protobuf_schema
from core.software.secure_boot import configure_secure_boot
from core.software.fatfs_config import configure_filesystem
from core.software.misra_checker import check_misra_compliance
from core.software.scheduler_sim import simulate_scheduler
from core.software.zigbee_mesh import design_zigbee_mesh
from core.software.cert_manager import generate_cert_config
from core.software.eeprom_wear import analyze_eeprom_wear
from core.software.fft_analyzer import analyze_fft_params
from core.software.log_framework import generate_log_framework
from core.software.unit_test_scaffold import generate_unit_test_scaffold
from core.software.code_size_analyzer import analyze_code_size
from core.software.firmware_diff import diff_firmware_binaries

from core.computer.web_stack import generate_web_api_architecture
from core.computer.microservices import generate_microservice_proto
from core.computer.frontend_gen import generate_react_component
from core.computer.code_complexity import audit_code_complexity
from core.computer.rest_api_gen import generate_rest_api_scaffold
from core.computer.ci_cd_pipeline import generate_ci_cd_pipeline
from core.computer.sql_schema_gen import generate_sql_schema
from core.computer.graphql_schema import generate_graphql_schema
from core.computer.terraform_gen import generate_terraform_module
from core.computer.auth_flow import generate_auth_flow
from core.computer.nginx_config import generate_nginx_config
from core.computer.rate_limit_design import design_rate_limiter
from core.computer.websocket_handler import generate_websocket_handler
from core.computer.nosql_model import design_nosql_model

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
from core.production.print_cost import estimate_3d_print_cost
from core.production.motor_sizing import size_motor
from core.production.bolt_torque import calculate_bolt_torque
from core.production.spring_design import design_spring
from core.production.gear_ratio import calculate_gear_ratio
from core.production.heatsink_design import design_heatsink
from core.production.tolerance_stack import analyze_tolerance_stack
from core.production.bearing_life import calculate_bearing_life
from core.production.print_settings import recommend_print_settings
from core.production.sheet_metal import calculate_sheet_metal_bend
from core.production.injection_mold import estimate_injection_mold
from core.production.cnc_feedrate import calculate_cnc_feedrate
from core.production.beam_stress import analyze_beam_stress
from core.production.vibration_analysis import analyze_vibration
from core.production.fan_selection import select_cooling_fan
from core.production.pipe_flow import calculate_pipe_flow
from core.production.solenoid_design import design_solenoid
from core.production.linear_actuator import select_linear_actuator
from core.production.encoder_resolution import calculate_encoder_resolution
from core.production.enclosure_ip import check_ip_rating_requirements



from core.engine.prompt_template import render_prompt_template
from core.engine.chain_of_thought import run_chain_of_thought
from core.infra.health_check import run_health_check
from core.infra.cron_scheduler import schedule_cron_job
from core.infra.env_manager import manage_env_config
from core.infra.retry_policy import execute_with_retry





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
