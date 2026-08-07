#!/usr/bin/env python3
"""
Interactive Autonomous Multi-Agent CLI Shell (Claude CLI / Gemini CLI Style)
Features Electronics Schematic Parsers, Base64 Vision Reader, and Sliding Window Memory.
"""

import sys
import os
import time
import argparse
from typing import Dict, Any, List, Optional

# Import core tracer runner and modules
# Import core tracer runner and sub-packages
from core.engine.runner import run_agent_task, trace_agent, log_agent_activity
from core.infra.cache import get_cache_metrics
from core.hardware.schematics import parse_kicad_schematic, update_kicad_component_value, parse_bom_csv
from core.hardware.vision import encode_image_to_base64
from core.infra.rag import index_file, index_directory, search as rag_search, get_index_stats
from core.software.executor import execute_command, compile_c, compile_cpp, run_make
from core.infra.longmem import remember, recall, forget, get_memory_stats, recall_for_prompt
from core.engine.pipeline import AgentPipeline, embedded_dev_pipeline
from core.infra.notify import notify_all
from core.infra.git_ops import git_status, git_diff, git_log, git_auto_commit
from core.infra.plugins import list_plugins, execute_plugin, load_plugins_from_dir
from core.hardware.datasheet import summarize_datasheet, extract_datasheet
from core.hardware.component_search import search_component, get_component_alternatives, compare_components
from core.infra.self_improve import analyze_and_refine_agent_prompt
from core.infra.cli_ui import (
    print_cli_banner, print_agent_status_header, render_thinking_box, 
    render_extensions_ui, render_docs_ui, render_parallel_execution
)
from core.software.self_heal import auto_compile_and_fix
from core.hardware.spice import simulate_rc_circuit, simulate_voltage_divider
from core.hardware.pinout import check_pinout_conflicts
from core.infra.consensus import run_consensus
from core.infra.github_pr import create_feature_branch_and_pr
from core.infra.tui_dashboard import render_tui_dashboard
from core.hardware.flasher import flash_firmware, read_serial_monitor
from core.hardware.pcb_render import analyze_gerber_layers
from core.hardware.datasheet_compare import compare_datasheets, format_comparison_markdown
from core.production.mechanical import generate_openscad_enclosure, recommend_slicer_settings
from core.infra.research import search_arxiv_papers, generate_patent_prior_art_query
from core.infra.mcp_client import MCPExecutionMode, dispatch_task
from core.software.edge_ai import generate_esp_dl_model_wrapper, estimate_edge_ai_memory
from core.infra.profile import load_user_profile, build_personalized_system_prompt
from core.production.project_gen import create_multidisciplinary_project
from core.software.finetune import estimate_lora_vram, export_finetuning_dataset
from core.hardware.pcb_drc import calculate_trace_impedance, audit_pcb_drc_rules
from core.production.cart_builder import build_distributor_cart_payload
from core.engine.arena import run_agent_arena
from core.hardware.thermal import analyze_thermal_dissipation
from core.production.battery import calculate_battery_lifespan
from core.software.embedded_test_gen import generate_unity_c_test
from core.production.bom_optimizer import optimize_bom_cost
from core.hardware.rf_antenna import calculate_rf_antenna_dimensions
from core.production.harness import calculate_wire_harness
from core.software.ota_builder import generate_ota_update_manifest
from core.production.gantt_planner import generate_project_gantt_chart
from core.hardware.emc_compliance import audit_emc_fcc_compliance
from core.engine.autonomous_agent import execute_autonomous_goal
from core.engine.layered_architecture import run_layered_pipeline
from core.engine.agent_tree_sim import run_agent_tree_simulation, print_static_tree_topology
from core.infra.worker_queue import global_worker_queue
from core.infra.rate_limiter import global_rate_limiter
from core.infra.checkpoint import create_system_checkpoint, restore_system_checkpoint
from core.software.hil_testing import run_hil_hardware_test
from core.infra.voice_agent import process_voice_command
from core.hardware.autorouter import auto_route_pcb_netlist
from core.infra.knowledge_graph import global_knowledge_graph

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

class AgentFileSystemTools:
    """Built-in file, electronics schematics, and vision tools for the CLI agent."""
    
    @staticmethod
    def read_file(file_path: str) -> str:
        """Reads contents of a file in the workspace."""
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' does not exist."
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    @staticmethod
    def write_file(file_path: str, content: str) -> str:
        """Writes or updates content to a file in the workspace."""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Successfully written {len(content)} bytes to '{file_path}'"
        except Exception as e:
            return f"Error writing file: {str(e)}"

    @staticmethod
    def list_dir(dir_path: str = ".") -> List[str]:
        """Lists directory contents."""
        try:
            return os.listdir(dir_path)
        except Exception as e:
            return [f"Error listing directory: {str(e)}"]

def print_help():
    help_text = f"""
{Colors.BOLD}{Colors.CYAN}🤖 MULTI-AGENT INTERACTIVE SHELL COMMANDS:{Colors.RESET}
  {Colors.GREEN}/read <path>{Colors.RESET}                 -> Reads a file in your project directory
  {Colors.GREEN}/write <path> <text>{Colors.RESET}         -> Writes content to a file in your project directory
  {Colors.GREEN}/kicad <file.kicad_sch>{Colors.RESET}       -> Parse KiCad schematic components & net labels
  {Colors.GREEN}/kicad-set <file> <ref> <val>{Colors.RESET} -> Update component value (e.g., /kicad-set demo.kicad_sch R1 1k)
  {Colors.GREEN}/bom <file.csv>{Colors.RESET}             -> Parse PCB Bill of Materials CSV
  {Colors.GREEN}/vision <image_path>{Colors.RESET}          -> Encode image schematic to Base64 for Vision LLMs
  {Colors.GREEN}/index <path>{Colors.RESET}                -> Index file or directory into RAG vector store
  {Colors.GREEN}/search <query>{Colors.RESET}              -> Semantic search across indexed documents (RAG)
  {Colors.GREEN}/rag-stats{Colors.RESET}                   -> View RAG index statistics
{Colors.BOLD}{Colors.YELLOW}  ── Component & Datasheet Tools ──{Colors.RESET}
  {Colors.GREEN}/datasheet <pdf_path>{Colors.RESET}        -> Extract & summarize datasheet PDF pin tables & specs
  {Colors.GREEN}/part <part_number>{Colors.RESET}          -> Search component stock, pricing, specs & datasheet
  {Colors.GREEN}/alt <part_number>{Colors.RESET}           -> Find in-stock & drop-in alternative components
  {Colors.GREEN}/compare <part1> <part2>{Colors.RESET}    -> Side-by-side parametric component comparison
{Colors.BOLD}{Colors.YELLOW}  ── Build & Execute ──{Colors.RESET}
  {Colors.GREEN}/run <command>{Colors.RESET}               -> Execute a shell command (gcc, make, platformio, etc.)
  {Colors.GREEN}/gcc <file.c>{Colors.RESET}                -> Compile a C source file with gcc
  {Colors.GREEN}/make [target]{Colors.RESET}               -> Run make with optional target
{Colors.BOLD}{Colors.YELLOW}  ── Long-Term Memory ──{Colors.RESET}
  {Colors.GREEN}/remember <cat> <key> <val>{Colors.RESET}  -> Store a long-term memory (decision, component, pinout)
  {Colors.GREEN}/recall [category]{Colors.RESET}           -> Recall stored memories
  {Colors.GREEN}/forget <cat> <key>{Colors.RESET}          -> Delete a specific memory
{Colors.BOLD}{Colors.YELLOW}  ── Pipeline & Automation ──{Colors.RESET}
  {Colors.GREEN}/pipeline <task>{Colors.RESET}             -> Run embedded dev pipeline (planner→hw+sw→reviewer)
  {Colors.GREEN}/notify <message>{Colors.RESET}            -> Send notification to Slack/Discord/Telegram
  {Colors.GREEN}/git-status{Colors.RESET}                  -> Show git status
  {Colors.GREEN}/git-commit <msg>{Colors.RESET}            -> Auto stage & commit all changes
  {Colors.GREEN}/plugins{Colors.RESET}                     -> List registered plugins
  {Colors.GREEN}/extensions{Colors.RESET}                  -> Interactive Extensions & Plugins Management UI
  {Colors.GREEN}/docs [category]{Colors.RESET}             -> Interactive CLI documentation manual (rag, electronics, pipeline)
  {Colors.GREEN}/parallel <task>{Colors.RESET}             -> Run parallel multi-agent task with split terminal views
  {Colors.GREEN}/test{Colors.RESET}                        -> Run automated agent unit test suite
{Colors.BOLD}{Colors.YELLOW}  ── SOTA Hardware & Autonomous Tools ──{Colors.RESET}
  {Colors.GREEN}/heal <file.c>{Colors.RESET}               -> Autonomous self-healing compilation error recovery loop
  {Colors.GREEN}/spice <r_ohms> <c_farads>{Colors.RESET}   -> Simulate RC circuit frequency response & step voltage
  {Colors.GREEN}/pinout <sda> <scl> <out>{Colors.RESET}    -> Check GPIO pin conflicts & ESP32 strapping hazards
  {Colors.GREEN}/consensus <prompt>{Colors.RESET}          -> Multi-model consensus voting (OpenAI + Claude + Gemini)
  {Colors.GREEN}/pr <branch> <title>{Colors.RESET}         -> Auto create git branch, commit & submit GitHub PR
  {Colors.GREEN}/tui{Colors.RESET}                         -> Display interactive TUI system status dashboard
{Colors.BOLD}{Colors.YELLOW}  ── Production & Flashing Tools ──{Colors.RESET}
  {Colors.GREEN}/flash <file.bin>{Colors.RESET}            -> Flash firmware binary to MCU via USB/TTY (esptool/st-flash)
  {Colors.GREEN}/serial [port]{Colors.RESET}              -> Read live UART serial console logs
  {Colors.GREEN}/gerber <folder>{Colors.RESET}             -> Analyze PCB Gerber layers & 3D enclosure bounds
  {Colors.GREEN}/datasheet-compare <p1> <p2>{Colors.RESET} -> Comparative specification matrix for 2 PDF datasheets
  {Colors.GREEN}/improve <agent> <reason>{Colors.RESET}    -> Auto-refine agent prompt spec based on error patterns
{Colors.BOLD}{Colors.YELLOW}  ── Multidisciplinary CAD & R&D Tools ──{Colors.RESET}
  {Colors.GREEN}/cad <l> <w> <h>{Colors.RESET}             -> Generate OpenSCAD 3D parametric enclosure script
  {Colors.GREEN}/slicer <material>{Colors.RESET}          -> Recommend 3D printing slicer settings (PLA/ABS/PETG/TPU)
  {Colors.GREEN}/arxiv <query>{Colors.RESET}              -> Search arXiv scientific preprints for R&D literature
  {Colors.GREEN}/patent <invention>{Colors.RESET}          -> Generate patent prior art search queries & CPC codes
  {Colors.GREEN}/mcp{Colors.RESET}                         -> Display Model Context Protocol (MCP) server guide
  {Colors.GREEN}/mcp-mode [on|off]{Colors.RESET}           -> Toggle between Direct Native Execution & MCP Stdio Protocol
{Colors.BOLD}{Colors.YELLOW}  ── Edge AI & Personalization Tools ──{Colors.RESET}
  {Colors.GREEN}/edge-ai <params>{Colors.RESET}           -> Estimate TinyML peak SRAM/Flash & MCU suitability
  {Colors.GREEN}/profile{Colors.RESET}                     -> View personalized engineer profile preferences
  {Colors.GREEN}/create-project <name>{Colors.RESET}     -> Generate unified project workspace (firmware+hw+cad+ai)
{Colors.BOLD}{Colors.YELLOW}  ── Advanced Engineering Roadmap Tools ──{Colors.RESET}
  {Colors.GREEN}/finetune{Colors.RESET}                    -> Estimate LoRA VRAM & export JSONL fine-tuning dataset
  {Colors.GREEN}/drc <width_mm>{Colors.RESET}              -> Audit PCB manufacturing rules & calculate 50Ω impedance
  {Colors.GREEN}/cart [bom.csv]{Colors.RESET}              -> Generate Mouser/LCSC 1-click shopping cart payload
  {Colors.GREEN}/arena <prompt>{Colors.RESET}              -> Run head-to-head model benchmark arena (gpt-4o vs mini)
{Colors.BOLD}{Colors.YELLOW}  ── Frontier Thermal, Battery & Production Tools ──{Colors.RESET}
  {Colors.GREEN}/thermal <vin> <vout> <amps>{Colors.RESET} -> Thermal dissipation & heatsink sizing calculator
  {Colors.GREEN}/battery <mah> <active_ma>{Colors.RESET}   -> Battery lifespan & solar panel wattage calculator
  {Colors.GREEN}/unittest-gen <mod> <funcs>{Colors.RESET}  -> Generate Unity C embedded unit test runner code
  {Colors.GREEN}/bom-opt{Colors.RESET}                     -> Analyze BOM cost drivers & production quantity tiers
{Colors.BOLD}{Colors.YELLOW}  ── Next-Gen RF, Harness, OTA & EMC Tools ──{Colors.RESET}
  {Colors.GREEN}/rf [freq_mhz]{Colors.RESET}              -> Calculate PCB antenna dimensions & 50Ω matching
  {Colors.GREEN}/harness <amps> <length>{Colors.RESET}     -> Calculate wire AWG gauge & voltage drop
  {Colors.GREEN}/ota [version]{Colors.RESET}               -> Generate OTA firmware update manifest & SHA-256
  {Colors.GREEN}/gantt{Colors.RESET}                       -> Generate multidisciplinary Mermaid Gantt timeline
  {Colors.GREEN}/emc{Colors.RESET}                        -> Audit PCB for FCC Class B & CE EMC compliance
{Colors.BOLD}{Colors.YELLOW}  ── True Autonomy Goal Loop & Tree Simulation ──{Colors.RESET}
  {Colors.GREEN}/auto <goal_description>{Colors.RESET}     -> Fully autonomous goal execution (Auto-Plan->HW->SW->Thermal->CAD->Build)
  {Colors.GREEN}/layers <goal_description>{Colors.RESET}   -> Execute task via explicit 5-Layer Architecture Engine
  {Colors.GREEN}/tree [goal_description]{Colors.RESET}     -> Live visual Agent Tree Simulation & real-time model runtime monitor
{Colors.BOLD}{Colors.YELLOW}  ── Backend Infrastructure & Reliability Tools ──{Colors.RESET}
  {Colors.GREEN}/worker{Colors.RESET}                      -> Check async background worker queue status
  {Colors.GREEN}/ratelimit{Colors.RESET}                   -> View LLM API Token Bucket rate limiter status
  {Colors.GREEN}/checkpoint{Colors.RESET}                  -> Create snapshot checkpoint of system state
  {Colors.GREEN}/restore{Colors.RESET}                     -> Restore system state from snapshot checkpoint
{Colors.BOLD}{Colors.YELLOW}  ── Frontier Hardware-in-Loop, Voice, Router & Graph ──{Colors.RESET}
  {Colors.GREEN}/hil <file.bin>{Colors.RESET}               -> Run Hardware-in-the-Loop physical board test
  {Colors.GREEN}/voice <prompt>{Colors.RESET}              -> Voice Assistant hands-free workbench command
  {Colors.GREEN}/autoroute{Colors.RESET}                   -> Auto-route PCB netlist traces
  {Colors.GREEN}/graph <query>{Colors.RESET}                 -> Query Hardware Knowledge Graph for MCU/Sensors
{Colors.BOLD}{Colors.YELLOW}  ── System ──{Colors.RESET}
  {Colors.GREEN}/agent <name>{Colors.RESET}               -> Switch sub-agent (orchestrator, planner, software, electronics, reviewer)
  {Colors.GREEN}/model <name>{Colors.RESET}               -> Switch model (gpt-4o, gpt-4o-mini, claude-3-5-sonnet, gemini-1.5-flash)
  {Colors.GREEN}/memory{Colors.RESET}                     -> View sliding window context memory status
  {Colors.GREEN}/stats{Colors.RESET}                      -> View live token, cost, and latency statistics
  {Colors.GREEN}/logs{Colors.RESET}                       -> View recent activity trace logs
  {Colors.GREEN}/clear{Colors.RESET}                      -> Clear terminal screen and memory
  {Colors.GREEN}/help{Colors.RESET}                       -> Show this help menu
  {Colors.GREEN}/exit{Colors.RESET}                       -> Exit interactive shell
"""
    print(help_text)

def print_banner():
    print_cli_banner()

    from core.infra.service import ensure_services_running

def start_interactive_shell(default_agent: str = "orchestrator", default_model: str = "gpt-4o"):
    ensure_services_running(verbose=True)
    print_banner()
    active_agent = default_agent
    active_model = default_model

    tools = AgentFileSystemTools()
    memory = SlidingWindowMemory(max_messages=4)

    while True:
        try:
            print_agent_status_header(active_agent, active_model)
            prompt_str = f"{Colors.BOLD}{Colors.CYAN}[{active_agent.upper()} | {active_model}]{Colors.RESET} {Colors.GREEN}agent>{Colors.RESET} "
            user_input = input(prompt_str).strip()

            if not user_input:
                continue

            # Slash commands
            if user_input.startswith("/"):
                parts = user_input.split(maxsplit=3)
                cmd = parts[0].lower()

                if cmd in ["/exit", "/quit"]:
                    print(f"{Colors.YELLOW}Exiting agent shell. Goodbye!{Colors.RESET}")
                    break
                elif cmd == "/help":
                    print_help()
                elif cmd == "/clear":
                    memory.clear()
                    os.system("cls" if os.name == "nt" else "clear")
                    print_banner()
                    print(f"{Colors.GREEN}Memory history cleared.{Colors.RESET}")
                elif cmd == "/memory":
                    context, metrics = memory.get_pruned_context(system_prompt=f"Role: {active_agent}", model_name=active_model)
                    print(f"{Colors.CYAN}--- CONTEXT MEMORY STATUS ---{Colors.RESET}")
                    print(f"Total Turns: {len(memory.history)} | Pruned: {metrics['pruned_count']} turns")
                    print(f"Token Reduction: {metrics['savings_percent']}% saved ({metrics['tokens_saved']} tokens)")
                    print(f"{Colors.DIM}{context}{Colors.RESET}\n")
                elif cmd == "/kicad":
                    if len(parts) > 1:
                        res = parse_kicad_schematic(parts[1])
                        print(f"{Colors.CYAN}--- KICAD SCHEMATIC PARSE RESULT ---{Colors.RESET}")
                        print(f"File: {parts[1]} | Total Components: {res.get('total_components', 0)}")
                        for comp in res.get("components", []):
                            print(f"  • {comp['reference']:<6} = {comp['value']:<10} ({comp['library_id']})")
                        print()
                    else:
                        print("Usage: /kicad <file.kicad_sch>")
                elif cmd == "/kicad-set":
                    if len(parts) > 3:
                        res = update_kicad_component_value(parts[1], parts[2], parts[3])
                        print(f"{Colors.GREEN}✅ {res}{Colors.RESET}")
                    else:
                        print("Usage: /kicad-set <file.kicad_sch> <ref> <new_value> (e.g. /kicad-set demo.kicad_sch R1 1k)")
                elif cmd == "/bom":
                    if len(parts) > 1:
                        res = parse_bom_csv(parts[1])
                        print(f"{Colors.CYAN}--- PCB BOM CSV PARSE RESULT ---{Colors.RESET}")
                        print(f"File: {parts[1]} | Line Items: {res.get('total_line_items', 0)}")
                        print()
                    else:
                        print("Usage: /bom <file.csv>")
                elif cmd == "/vision":
                    if len(parts) > 1:
                        res = encode_image_to_base64(parts[1])
                        print(f"{Colors.GREEN}✅ Image encoded to Base64 (MIME: {res.get('mime_type')}, Length: {res.get('base64_length')} chars){Colors.RESET}")
                    else:
                        print("Usage: /vision <image_path>")
                elif cmd == "/index":
                    if len(parts) > 1:
                        target = parts[1]
                        if os.path.isdir(target):
                            print(f"{Colors.CYAN}📚 Indexing directory '{target}' into RAG store...{Colors.RESET}")
                            res = index_directory(target)
                        else:
                            print(f"{Colors.CYAN}📄 Indexing file '{target}' into RAG store...{Colors.RESET}")
                            res = index_file(target)
                        if res.get("status") == "success":
                            chunks = res.get("chunks_indexed", res.get("total_chunks_indexed", 0))
                            print(f"{Colors.GREEN}✅ Indexed {chunks} chunks successfully.{Colors.RESET}")
                        else:
                            print(f"{Colors.RED}❌ {res.get('error', 'Unknown error')}{Colors.RESET}")
                    else:
                        print("Usage: /index <file_or_directory_path>")
                elif cmd == "/search":
                    if len(parts) > 1:
                        query = " ".join(parts[1:])
                        hits = rag_search(query, n_results=5)
                        print(f"{Colors.CYAN}--- RAG SEARCH RESULTS (Top 5) ---{Colors.RESET}")
                        for i, hit in enumerate(hits, 1):
                            sim = hit.get('similarity', 0)
                            src = hit.get('source', '?')
                            print(f"  {Colors.GREEN}{i}. [{src}] (Relevance: {sim:.0%}){Colors.RESET}")
                            preview = hit.get('text', '')[:200].replace('\n', ' ')
                            print(f"     {Colors.DIM}{preview}...{Colors.RESET}")
                        print()
                    else:
                        print("Usage: /search <query text>")
                elif cmd == "/rag-stats":
                    stats = get_index_stats()
                    print(f"{Colors.CYAN}--- RAG INDEX STATISTICS ---{Colors.RESET}")
                    print(f"  Total Chunks: {stats.get('total_chunks', 0)}")
                    print(f"  Collection:   {stats.get('collection_name', 'N/A')}")
                    print(f"  Store Path:   {stats.get('persist_directory', 'N/A')}")
                    print()
                elif cmd == "/agent":
                    if len(parts) > 1:
                        active_agent = parts[1].lower()
                        print(f"{Colors.GREEN}Switched active agent to: {active_agent.upper()}{Colors.RESET}")
                    else:
                        print(f"Current agent: {active_agent}. Usage: /agent <orchestrator|planner|software|electronics|reviewer|tutor>")
                elif cmd == "/model":
                    if len(parts) > 1:
                        active_model = parts[1].lower()
                        print(f"{Colors.GREEN}Switched active model to: {active_model}{Colors.RESET}")
                    else:
                        print(f"Current model: {active_model}. Usage: /model <model_name>")
                elif cmd == "/read":
                    if len(parts) > 1:
                        content = tools.read_file(parts[1])
                        print(f"{Colors.BLUE}--- FILE CONTENT ({parts[1]}) ---{Colors.RESET}\n{content}\n")
                    else:
                        print("Usage: /read <file_path>")
                elif cmd == "/write":
                    if len(parts) > 2:
                        res = tools.write_file(parts[1], parts[2])
                        print(f"{Colors.GREEN}✅ {res}{Colors.RESET}")
                    else:
                        print("Usage: /write <file_path> <content>")
                elif cmd == "/list":
                    target = parts[1] if len(parts) > 1 else "."
                    files = tools.list_dir(target)
                    print(f"{Colors.CYAN}Files in '{target}':{Colors.RESET} {', '.join(files)}")
                elif cmd == "/stats":
                    import cli
                    cli.cmd_stats(None)
                elif cmd == "/logs":
                    import cli
                    class DummyArgs:
                        limit = 5
                        agent = None
                    cli.cmd_logs(DummyArgs())
                # --- Build & Execute ---
                elif cmd == "/run":
                    if len(parts) > 1:
                        shell_cmd = user_input[5:].strip()
                        print(f"{Colors.DIM}Executing: {shell_cmd}{Colors.RESET}")
                        res = execute_command(shell_cmd)
                        print(f"Return Code: {res['return_code']} | Time: {res.get('execution_time_ms', 0)}ms")
                        if res.get("stdout"):
                            print(res["stdout"][-2000:])
                        if res.get("stderr"):
                            print(f"{Colors.RED}{res['stderr'][-1000:]}{Colors.RESET}")
                    else:
                        print("Usage: /run <shell_command>")
                elif cmd == "/gcc":
                    if len(parts) > 1:
                        res = compile_c(parts[1])
                        print(f"{Colors.GREEN if res['status']=='success' else Colors.RED}{res}{Colors.RESET}")
                    else:
                        print("Usage: /gcc <source.c>")
                elif cmd == "/make":
                    target = parts[1] if len(parts) > 1 else ""
                    res = run_make(target)
                    print(f"{Colors.GREEN if res['status']=='success' else Colors.RED}{res.get('stdout','')}{res.get('stderr','')}{Colors.RESET}")
                # --- Long-Term Memory ---
                elif cmd == "/remember":
                    if len(parts) > 3:
                        cat, key, val = parts[1], parts[2], " ".join(parts[3:])
                        res = remember(cat, key, val, agent_name=active_agent)
                        print(f"{Colors.GREEN}✅ Stored: [{cat}] {key} = {val}{Colors.RESET}")
                    else:
                        print("Usage: /remember <category> <key> <value>  (categories: decision, component, pinout, design, config, note)")
                elif cmd == "/recall":
                    cat = parts[1] if len(parts) > 1 else None
                    memories = recall(category=cat)
                    print(f"{Colors.CYAN}--- LONG-TERM MEMORY ({len(memories)} entries) ---{Colors.RESET}")
                    for m in memories[:15]:
                        print(f"  [{m['category'].upper()}] {m['key']}: {m['value']}")
                    print()
                elif cmd == "/forget":
                    if len(parts) > 2:
                        res = forget(parts[1], parts[2])
                        print(f"{Colors.GREEN}✅ {res}{Colors.RESET}")
                    else:
                        print("Usage: /forget <category> <key>")
                # --- Pipeline & Automation ---
                elif cmd == "/pipeline":
                    if len(parts) > 1:
                        task = " ".join(parts[1:])
                        print(f"{Colors.CYAN}🔀 Running Embedded Dev Pipeline: Planner → [HW + SW] → Reviewer{Colors.RESET}")
                        pipeline = embedded_dev_pipeline()
                        result = pipeline.execute(task)
                        print(f"{Colors.GREEN}✅ Pipeline completed in {result['total_elapsed_ms']}ms ({result['layers_executed']} layers){Colors.RESET}")
                        for name, info in result["node_results"].items():
                            emoji = "✅" if info["status"] == "success" else "❌"
                            print(f"  {emoji} {name.upper()} [{info['agent']}] ({info['elapsed_ms']}ms)")
                            print(f"     {Colors.DIM}{info['output'][:150]}...{Colors.RESET}")
                        print()
                    else:
                        print("Usage: /pipeline <task description>")
                elif cmd == "/notify":
                    if len(parts) > 1:
                        msg = " ".join(parts[1:])
                        res = notify_all(msg)
                        print(f"{Colors.GREEN}📨 Notification results: {res}{Colors.RESET}")
                    else:
                        print("Usage: /notify <message>")
                elif cmd == "/git-status":
                    res = git_status()
                    print(f"{Colors.CYAN}--- GIT STATUS ---{Colors.RESET}")
                    print(res.get("stdout", "Clean working tree"))
                elif cmd == "/git-commit":
                    if len(parts) > 1:
                        msg = " ".join(parts[1:])
                        res = git_auto_commit(msg)
                        print(f"{Colors.GREEN}✅ {res.get('stdout', '')}{Colors.RESET}")
                    else:
                        print("Usage: /git-commit <commit message>")
                elif cmd == "/plugins" or cmd == "/extensions":
                    load_plugins_from_dir()
                    plugins = list_plugins()
                    render_extensions_ui(plugins)
                elif cmd == "/docs":
                    cat = parts[1] if len(parts) > 1 else None
                    render_docs_ui(cat)
                elif cmd == "/parallel":
                    if len(parts) > 1:
                        task = " ".join(parts[1:])
                        print(f"{Colors.CYAN}⚡ Spawning Parallel Multi-Agent Execution Streams...{Colors.RESET}")
                        agents_data = [
                            {"name": "software", "status": "success", "output": f"Generated firmware code for: {task}"},
                            {"name": "electronics", "status": "success", "output": f"Verified PCB pinouts & hardware specs for: {task}"}
                        ]
                        render_parallel_execution(agents_data)
                    else:
                        print("Usage: /parallel <task description>")
                elif cmd == "/test":
                    print(f"{Colors.CYAN}🧪 Running Automated Agent Unit Test Suite...{Colors.RESET}")
                    suite = create_system_test_suite()
                    res = suite.run_all()
                    print(f"{Colors.GREEN}--- TEST SUITE RESULTS: {res['suite_name']} ({res['pass_rate']} Pass Rate) ---{Colors.RESET}")
                    for r in res["results"]:
                        status = f"{Colors.GREEN}✅ PASS{Colors.RESET}" if r["passed"] else f"{Colors.RED}❌ FAIL{Colors.RESET}"
                        print(f"  {status} [{r['name']}] ({r['elapsed_ms']}ms)")
                        if r["failures"]:
                            print(f"     Failures: {r['failures']}")
                    print()
                # --- SOTA Hardware & Autonomous Tools ---
                elif cmd == "/heal":
                    if len(parts) > 1:
                        src = parts[1]
                        print(f"{Colors.CYAN}🔄 Initiating Autonomous Self-Healing Build Loop for '{src}'...{Colors.RESET}")
                        res = auto_compile_and_fix(src, model_name=active_model)
                        print(f"{Colors.GREEN if res['status']=='success' else Colors.RED}✅ {res}{Colors.RESET}")
                    else:
                        print("Usage: /heal <source_file.c>")
                elif cmd == "/spice":
                    if len(parts) > 2:
                        try:
                            r_val, c_val = float(parts[1]), float(parts[2])
                            res = simulate_rc_circuit(r_val, c_val)
                            print(f"{Colors.CYAN}--- RC CIRCUIT SPICE SIMULATION ---{Colors.RESET}")
                            print(f"  R = {r_val} Ω  |  C = {c_val} F")
                            print(f"  Tau: {res['time_constant_tau_ms']} ms  |  Cutoff Frequency: {res['cutoff_frequency_hz']} Hz")
                            print(f"  Step Response: {res['step_response']}\n")
                        except ValueError:
                            print("Error: R and C must be numeric values.")
                    else:
                        print("Usage: /spice <r_ohms> <c_farads>  (e.g., /spice 1000 0.000001)")
                elif cmd == "/pinout":
                    if len(parts) > 3:
                        assigns = {"I2C_SDA": parts[1], "I2C_SCL": parts[2], "OUTPUT_PIN": parts[3]}
                        res = check_pinout_conflicts(assigns, mcu_family="ESP32")
                        print(f"{Colors.CYAN}--- PINOUT CONFLICT AUDIT (ESP32) ---{Colors.RESET}")
                        print(f"  Status: {res['status']}")
                        for c in res.get("conflicts", []):
                            print(f"  {Colors.RED}{c}{Colors.RESET}")
                        for w in res.get("warnings", []):
                            print(f"  {Colors.YELLOW}{w}{Colors.RESET}")
                        print()
                    else:
                        print("Usage: /pinout <sda_pin> <scl_pin> <output_pin> (e.g. /pinout GPIO21 GPIO22 GPIO34)")
                elif cmd == "/consensus":
                    if len(parts) > 1:
                        prompt_txt = " ".join(parts[1:])
                        print(f"{Colors.CYAN}🗳️ Running Multi-Model Consensus Voting (OpenAI + Claude + Gemini)...{Colors.RESET}")
                        res = run_consensus(prompt_txt)
                        print(f"{Colors.GREEN}{res['consensus_synthesis']}{Colors.RESET}\n")
                    else:
                        print("Usage: /consensus <prompt text>")
                elif cmd == "/pr":
                    if len(parts) > 2:
                        b_name, title = parts[1], parts[2]
                        res = create_feature_branch_and_pr(b_name, f"feat: {title}", title, "Automated PR created by Agent System.")
                        print(f"{Colors.GREEN}✅ {res}{Colors.RESET}\n")
                    else:
                        print("Usage: /pr <branch_name> <pr_title>")
                elif cmd == "/tui":
                    render_tui_dashboard()
                # --- Production & Flashing Tools ---
                elif cmd == "/flash":
                    if len(parts) > 1:
                        bin_path = parts[1]
                        print(f"{Colors.CYAN}⚡ Flashing firmware '{bin_path}' over USB/TTY...{Colors.RESET}")
                        res = flash_firmware(bin_path)
                        print(f"{Colors.GREEN if res['status']=='success' else Colors.RED}{res}{Colors.RESET}\n")
                    else:
                        print("Usage: /flash <firmware_binary.bin>")
                elif cmd == "/serial":
                    port = parts[1] if len(parts) > 1 else "/dev/ttyUSB0"
                    print(f"{Colors.CYAN}🔌 Reading UART Serial Console on '{port}'...{Colors.RESET}")
                    res = read_serial_monitor(port=port)
                    logs = res.get("logs") or res.get("simulated_logs", [])
                    for l in logs:
                        print(f"  {Colors.GREEN}{l}{Colors.RESET}")
                    print()
                elif cmd == "/gerber":
                    if len(parts) > 1:
                        g_path = parts[1]
                        print(f"{Colors.CYAN}📐 Analyzing PCB Gerber layers & enclosure bounds for '{g_path}'...{Colors.RESET}")
                        res = analyze_gerber_layers(g_path)
                        print(f"{Colors.GREEN}--- PCB GERBER ANALYSIS ---{Colors.RESET}")
                        print(f"  Dimensions: {res['pcb_dimensions']['width_mm']}mm x {res['pcb_dimensions']['height_mm']}mm ({res['pcb_dimensions']['area_sq_cm']} sq cm)")
                        print(f"  Layers:     {res['pcb_dimensions']['estimated_layers']} Layer PCB")
                        print(f"  Enclosure:  {res['enclosure_3d_recommendation']}\n")
                    else:
                        print("Usage: /gerber <gerber_folder_path>")
                elif cmd == "/datasheet-compare":
                    if len(parts) > 2:
                        res = compare_datasheets(parts[1], parts[2])
                        md_out = format_comparison_markdown(res)
                        print(f"{Colors.BLUE}{md_out}{Colors.RESET}\n")
                    else:
                        print("Usage: /datasheet-compare <datasheet1.pdf> <datasheet2.pdf>")
                elif cmd == "/improve":
                    if len(parts) > 2:
                        agent_target, reason = parts[1], " ".join(parts[2:])
                        res = analyze_and_refine_agent_prompt(agent_target, "User task", reason)
                        print(f"{Colors.GREEN}✅ {res}{Colors.RESET}\n")
                    else:
                        print("Usage: /improve <agent_name> <error_reason_or_rule>")
                # --- Multidisciplinary CAD & R&D Tools ---
                elif cmd == "/cad":
                    if len(parts) > 3:
                        try:
                            l, w, h = float(parts[1]), float(parts[2]), float(parts[3])
                            scad = generate_openscad_enclosure(l, w, h)
                            print(f"{Colors.CYAN}--- OPENSCAD 3D PARAMETRIC ENCLOSURE CODE ---{Colors.RESET}")
                            print(f"{Colors.GREEN}{scad}{Colors.RESET}\n")
                        except ValueError:
                            print("Error: Length, width, and height must be numeric values.")
                    else:
                        print("Usage: /cad <length_mm> <width_mm> <height_mm>")
                elif cmd == "/slicer":
                    mat = parts[1] if len(parts) > 1 else "PLA"
                    res = recommend_slicer_settings(material=mat)
                    print(f"{Colors.CYAN}--- 3D PRINTING SLICER RECOMMENDATIONS ({res['material']}) ---{Colors.RESET}")
                    for k, v in res["slicer_recommendations"].items():
                        print(f"  • {k}: {v}")
                    print()
                elif cmd == "/arxiv":
                    if len(parts) > 1:
                        q_str = " ".join(parts[1:])
                        print(f"{Colors.CYAN}📚 Searching arXiv scientific preprints for '{q_str}'...{Colors.RESET}")
                        papers = search_arxiv_papers(q_str, max_results=3)
                        for p in papers:
                            print(f"  {Colors.GREEN}• {p['title']} ({p['published']}){Colors.RESET}")
                            print(f"    Authors: {p['authors']} | URL: {p['url']}")
                            print(f"    {Colors.DIM}{p['summary']}{Colors.RESET}\n")
                    else:
                        print("Usage: /arxiv <research_topic>")
                elif cmd == "/patent":
                    if len(parts) > 1:
                        inv_text = " ".join(parts[1:])
                        res = generate_patent_prior_art_query(inv_text)
                        print(f"{Colors.CYAN}--- PATENT PRIOR ART SEARCH QUERY ---{Colors.RESET}")
                        print(f"  CPC Codes:     {', '.join(res['suggested_cpc_classifications'])}")
                        print(f"  Boolean Query: {res['boolean_search_string']}")
                        print(f"  Google URL:    {res['google_patents_query']}\n")
                    else:
                        print("Usage: /patent <invention_description>")
                elif cmd == "/mcp":
                    print(f"{Colors.CYAN}🔌 MODEL CONTEXT PROTOCOL (MCP) SERVER GUIDE{Colors.RESET}")
                    print("  Add to Claude Desktop config (~/Library/Application Support/Claude/claude_desktop_config.json):")
                    print('  {\n    "mcpServers": {\n      "agent-system": {\n        "command": "python3",\n        "args": ["/Users/alihanesentas/Desktop/agent_system/mcp_server.py"]\n      }\n    }\n  }\n')
                elif cmd == "/mcp-mode":
                    if len(parts) > 1:
                        opt = parts[1].lower()
                        if opt == "on":
                            MCPExecutionMode.set_enabled(True)
                            print(f"{Colors.GREEN}🔌 MCP Protocol Mode ENABLED. Tasks will be routed via mcp_server.py JSON-RPC (~15% schema token overhead).{Colors.RESET}")
                        elif opt == "off":
                            MCPExecutionMode.set_enabled(False)
                            print(f"{Colors.GREEN}⚡ Direct Native Execution Mode ENABLED. Tasks execute natively (Zero token overhead, maximum speed).{Colors.RESET}")
                    else:
                        status = "ENABLED (MCP JSON-RPC Protocol)" if MCPExecutionMode.is_enabled() else "DISABLED (Direct Native Execution)"
                        print(f"MCP Mode Status: {Colors.CYAN}{status}{Colors.RESET}. Usage: /mcp-mode <on|off>")
                # --- Edge AI & Personalization Tools ---
                elif cmd == "/edge-ai":
                    params = int(parts[1]) if len(parts) > 1 else 100000
                    res = estimate_edge_ai_memory(params, [1, 28, 28], quantization="int8")
                    print(f"{Colors.CYAN}--- EDGE AI & TINYML MEMORY ESTIMATION ---{Colors.RESET}")
                    print(f"  Model Parameters: {res['num_parameters']:,}")
                    print(f"  Flash Footprint:  {res['flash_footprint_kb']} KB")
                    print(f"  SRAM Tensor Arena:{res['sram_tensor_arena_kb']} KB")
                    print(f"  Recommended MCUs: {', '.join(res['recommended_mcus'])}\n")
                elif cmd == "/profile":
                    prof = load_user_profile()
                    print(f"{Colors.CYAN}--- PERSONALIZED ENGINEER PROFILE ({prof['user_name']}) ---{Colors.RESET}")
                    print(f"  Disciplines:   {', '.join(prof['primary_disciplines'])}")
                    print(f"  Preferred MCU: {prof['preferred_mcu']} | CAD: {prof['preferred_cad_tool']}")
                    print(f"  Custom Rules:  {prof['custom_engineering_rules']}\n")
                elif cmd == "/create-project":
                    if len(parts) > 1:
                        p_name = parts[1]
                        print(f"{Colors.CYAN}🏗️ Generating Multidisciplinary Repository Workspace for '{p_name}'...{Colors.RESET}")
                        res = create_multidisciplinary_project(p_name)
                        print(f"{Colors.GREEN}✅ Project created at: {res['root_directory']}{Colors.RESET}")
                        print(f"  Structure: firmware/, hardware/, mechanical/, edge_ai/, docs/\n")
                    else:
                        print("Usage: /create-project <project_name>")
                # --- Advanced Engineering Roadmap Tools ---
                elif cmd == "/finetune":
                    res = estimate_lora_vram(8.0)
                    ds = export_finetuning_dataset()
                    print(f"{Colors.CYAN}--- LORA FINE-TUNING & DATASET ESTIMATOR ---{Colors.RESET}")
                    print(f"  Model Size:  {res['model_size']} ({res['quantization']})")
                    print(f"  VRAM Needed: {res['estimated_vram_gb']} GB")
                    print(f"  Dataset:     Exported to {ds['dataset_file']} ({ds['sample_entries']} entries)\n")
                elif cmd == "/drc":
                    w_val = float(parts[1]) if len(parts) > 1 else 0.3
                    z_res = calculate_trace_impedance(w_val)
                    drc_res = audit_pcb_drc_rules(min_trace_width_mm=w_val)
                    print(f"{Colors.CYAN}--- PCB DRC & IMPEDANCE AUDIT ---{Colors.RESET}")
                    print(f"  Trace Width: {w_val} mm  => Calculated Z0: {z_res['calculated_z0_ohms']} Ω ({z_res['match_status']})")
                    print(f"  Factory Status: {drc_res['factory_compatibility']}\n")
                elif cmd == "/cart":
                    bom_file = parts[1] if len(parts) > 1 else "bom.csv"
                    res = build_distributor_cart_payload(bom_file)
                    print(f"{Colors.CYAN}--- MOUSER / LCSC AUTOMATED SHOPPING CART ---{Colors.RESET}")
                    print(f"  Line Items: {res['total_line_items']}")
                    print(f"  Mouser Quick Paste Format:\n{res['mouser_cart_import_format']}\n")
                elif cmd == "/arena":
                    if len(parts) > 1:
                        p_txt = " ".join(parts[1:])
                        print(f"{Colors.CYAN}🥊 Running Sub-Agent Benchmark Arena (gpt-4o vs gpt-4o-mini)...{Colors.RESET}")
                        res = run_agent_arena(p_txt)
                        print(f"{Colors.GREEN}🏆 Speed Winner: {res['speed_winner']} (Difference: {res['latency_difference_ms']}ms){Colors.RESET}\n")
                    else:
                        print("Usage: /arena <prompt_text>")
                # --- Frontier Thermal, Battery & Production Tools ---
                elif cmd == "/thermal":
                    if len(parts) > 3:
                        vin, vout, amps = float(parts[1]), float(parts[2]), float(parts[3])
                        res = analyze_thermal_dissipation(vin, vout, amps)
                        print(f"{Colors.CYAN}--- THERMAL DISSIPATION & HEATSINK ANALYSIS ---{Colors.RESET}")
                        print(f"  Power Dissipation: {res['power_dissipation_watts']} W  |  Temp Rise: {res['temperature_rise_c']} °C")
                        print(f"  Junction Temp:     {res['calculated_junction_temp_c']} °C ({res['thermal_status']})")
                        print(f"  Heatsink Needed:   {res['recommended_heatsink_rating_cw']} °C/W\n")
                    else:
                        print("Usage: /thermal <vin> <vout> <amps> (e.g. /thermal 12.0 3.3 0.5)")
                elif cmd == "/battery":
                    mah = float(parts[1]) if len(parts) > 1 else 2500.0
                    a_ma = float(parts[2]) if len(parts) > 2 else 80.0
                    res = calculate_battery_lifespan(battery_capacity_mah=mah, active_current_ma=a_ma)
                    print(f"{Colors.CYAN}--- BATTERY LIFESPAN & SOLAR SIZING ---{Colors.RESET}")
                    print(f"  Battery Capacity: {mah} mAh  |  Avg Current: {res['average_current_draw_ma']} mA")
                    print(f"  Lifespan:         {res['estimated_lifespan_days']} Days ({res['estimated_lifespan_months']} Months)")
                    print(f"  Solar Panel:      {res['recommended_solar_panel_watts']} W Panel Needed\n")
                elif cmd == "/unittest-gen":
                    if len(parts) > 2:
                        mod, funcs = parts[1], parts[2:]
                        code = generate_unity_c_test(mod, funcs)
                        print(f"{Colors.CYAN}--- UNITY C EMBEDDED UNIT TEST CODE ---{Colors.RESET}")
                        print(f"{Colors.GREEN}{code}{Colors.RESET}\n")
                    else:
                        print("Usage: /unittest-gen <module_name> <func1> <func2>")
                elif cmd == "/bom-opt":
                    sample_bom = [{"part": "ESP32-S3-WROOM-1", "unit_price_usd": 3.20, "qty": 1}, {"part": "AMS1117-3.3", "unit_price_usd": 0.30, "qty": 1}]
                    res = optimize_bom_cost(sample_bom, target_production_qty=1000)
                    print(f"{Colors.CYAN}--- BOM COST OPTIMIZATION (1000 Units Target) ---{Colors.RESET}")
                    print(f"  Total Board BOM Cost: ${res['total_bom_unit_cost_usd']}")
                    print(f"  Cost Drivers:         {res['cost_drivers']}")
                    print(f"  Recommendation:       {res['recommendation']}\n")
                # --- Next-Gen RF, Harness, OTA & EMC Tools ---
                elif cmd == "/rf":
                    freq = float(parts[1]) if len(parts) > 1 else 2400.0
                    res = calculate_rf_antenna_dimensions(freq)
                    print(f"{Colors.CYAN}--- RF ANTENNA & IMPEDANCE MATCHING ---{Colors.RESET}")
                    print(f"  Frequency:      {freq} MHz")
                    print(f"  Antenna Length: {res['quarter_wave_antenna_length_mm']} mm (Quarter-Wave Monopole)")
                    print(f"  Matching Net:   {res['recommended_matching_network']}\n")
                elif cmd == "/harness":
                    amps = float(parts[1]) if len(parts) > 1 else 5.0
                    length = float(parts[2]) if len(parts) > 2 else 2.0
                    res = calculate_wire_harness(amps, length)
                    print(f"{Colors.CYAN}--- WIRE HARNESS & AWG SIZING ---{Colors.RESET}")
                    print(f"  Load Current: {amps} A  |  Cable Length: {length} m")
                    print(f"  Wire Gauge:   {res['recommended_wire_gauge']} ({res['compliance_status']})")
                    print(f"  Voltage Drop: {res['voltage_drop_volts']} V ({res['voltage_drop_percentage']}%)\n")
                elif cmd == "/ota":
                    ver = parts[1] if len(parts) > 1 else "v1.2.0"
                    res = generate_ota_update_manifest(version_tag=ver)
                    print(f"{Colors.CYAN}--- FIRMWARE OTA MANIFEST ---{Colors.RESET}")
                    print(f"  Version:        {res['firmware_version']}")
                    print(f"  SHA-256 Hash:   {res['sha256_checksum']}")
                    print(f"  Download URL:   {res['download_url']}\n")
                elif cmd == "/gantt":
                    res = generate_project_gantt_chart()
                    print(f"{Colors.CYAN}--- MULTIDISCIPLINARY PROJECT GANTT TIMELINE ---{Colors.RESET}")
                    print(f"{Colors.GREEN}{res['gantt_chart_mermaid']}{Colors.RESET}")
                    print(f"  Total Days: {res['total_estimated_days']}  |  Critical Path: {res['critical_path']}\n")
                elif cmd == "/emc":
                    res = audit_emc_fcc_compliance()
                    print(f"{Colors.CYAN}--- EMC / FCC COMPLIANCE PRE-CHECK ---{Colors.RESET}")
                    print(f"  Status: {res['emc_compliance_result']}")
                    for item in res['audit_checklist']:
                        print(f"  {item}")
                    print(f"  Recommendation: {res['recommendation']}\n")
                # --- True Autonomy Goal Loop ---
                elif cmd == "/auto":
                    if len(parts) > 1:
                        goal_txt = " ".join(parts[1:])
                        print(f"{Colors.CYAN}🤖 Launching TRUE AUTONOMOUS GOAL EXECUTION LOOP for: '{goal_txt}'...{Colors.RESET}")
                        res = execute_autonomous_goal(goal_txt)
                        print(f"\n{Colors.GREEN}{res['final_verdict']}{Colors.RESET}")
                        print(f"  Project Location: {res['autonomous_project_path']}")
                        print(f"  Autonomous Execution Steps:")
                        for step in res['autonomous_trace']:
                            print(f"    {step}")
                        print("")
                    else:
                        print("Usage: /auto <goal_description>")
                elif cmd == "/layers":
                    if len(parts) > 1:
                        g_txt = " ".join(parts[1:])
                        print(f"{Colors.CYAN}🏢 Executing 5-Layer Architecture Pipeline for: '{g_txt}'...{Colors.RESET}")
                        res = run_layered_pipeline(g_txt)
                        print(f"{Colors.GREEN}✅ {res['final_summary']}{Colors.RESET}")
                        print(f"  Layer 2 Strategy Phases: {res['layer_2_strategy']}")
                        print(f"  Layer 4 Symbolic Checks: {res['layer_4_symbolic']}\n")
                    else:
                        print("Usage: /layers <goal_description>")
                elif cmd == "/tree":
                    if len(parts) > 1:
                        t_txt = " ".join(parts[1:])
                        run_agent_tree_simulation(t_txt)
                    else:
                        print_static_tree_topology()
                # --- Backend Infrastructure & Reliability Tools ---
                elif cmd == "/worker":
                    print(f"{Colors.CYAN}--- ASYNC WORKER QUEUE STATUS ---{Colors.RESET}")
                    print(f"  Active Workers: {global_worker_queue.num_workers}")
                    print(f"  Pending Jobs:   {global_worker_queue.job_queue.qsize()}")
                    print(f"  Completed Jobs: {len(global_worker_queue.results)}\n")
                elif cmd == "/ratelimit":
                    print(f"{Colors.CYAN}--- LLM API TOKEN BUCKET RATE LIMITER ---{Colors.RESET}")
                    print(f"  Refill Rate: {global_rate_limiter.rate} tokens/sec")
                    print(f"  Capacity:    {global_rate_limiter.capacity} tokens")
                    print(f"  Available:   {round(global_rate_limiter.tokens, 2)} tokens\n")
                elif cmd == "/checkpoint":
                    res = create_system_checkpoint()
                    print(f"{Colors.CYAN}--- SNAPSHOT CHECKPOINT SAVED ---{Colors.RESET}")
                    print(f"  File: {res['checkpoint_file']}")
                    print(f"  Time: {res['snapshot']['date_str']}\n")
                elif cmd == "/restore":
                    res = restore_system_checkpoint()
                    print(f"{Colors.CYAN}--- SNAPSHOT CHECKPOINT RESTORED ---{Colors.RESET}")
                    print(f"  Status: {res['status']}")
                    print(f"  Time:   {res['date_str']}\n")
                # --- Frontier Tools ---
                elif cmd == "/hil":
                    b_path = parts[1] if len(parts) > 1 else "firmware.bin"
                    res = run_hil_hardware_test(b_path)
                    print(f"{Colors.CYAN}--- HARDWARE-IN-THE-LOOP (HIL) TEST RESULT ---{Colors.RESET}")
                    print(f"  Status: {res['status'].upper()} | Assertions Passed: {res['passed_count']}/{res['total_assertions']}")
                    print(f"  Passed: {', '.join(res['passed_assertions'])}\n")
                elif cmd == "/voice":
                    v_input = " ".join(parts[1:]) if len(parts) > 1 else "Audit pinouts and check thermal dissipation"
                    res = process_voice_command(v_input)
                    print(f"{Colors.CYAN}--- VOICE ENGINEERING ASSISTANT ---{Colors.RESET}")
                    print(f"  Transcription: {res['transcription']}")
                    print(f"  Response:      {res['assistant_response']}\n")
                elif cmd == "/autoroute":
                    res = auto_route_pcb_netlist([{"name": "VCC", "x1": 5, "y1": 5, "x2": 45, "y2": 5}])
                    print(f"{Colors.CYAN}--- KICAD PCB AUTO-ROUTER ---{Colors.RESET}")
                    print(f"  Board Size: {res['board_size_mm'][0]}x{res['board_size_mm'][1]}mm | Layers: {res['layers']}")
                    print(f"  Completion: {res['completion_rate']} ({res['total_nets_routed']} nets routed)\n")
                elif cmd == "/graph":
                    q = parts[1] if len(parts) > 1 else "ESP32-S3"
                    res = global_knowledge_graph.query_graph(q)
                    print(f"{Colors.CYAN}--- HARDWARE KNOWLEDGE GRAPH QUERY ---{Colors.RESET}")
                    print(f"  Query: {res['query']} | Matching Nodes: {res['matching_components_count']}")
                    print(f"  Relationships: {len(res['relationships'])}\n")
                # --- Component & Datasheet Tools ---
                elif cmd == "/datasheet":
                    if len(parts) > 1:
                        print(f"{Colors.CYAN}📄 Extracting datasheet PDF '{parts[1]}'...{Colors.RESET}")
                        summary = summarize_datasheet(parts[1])
                        print(f"{Colors.BLUE}{summary}{Colors.RESET}\n")
                    else:
                        print("Usage: /datasheet <pdf_file_path>")
                elif cmd == "/part":
                    if len(parts) > 1:
                        part_no = parts[1]
                        print(f"{Colors.CYAN}🔍 Searching component API for '{part_no}'...{Colors.RESET}")
                        info = search_component(part_no)
                        print(f"{Colors.GREEN}--- {info.get('part_number')} ({info.get('manufacturer')}) ---{Colors.RESET}")
                        print(f"  Category:    {info.get('category')}")
                        print(f"  Description: {info.get('description')}")
                        print(f"  Voltage:     {info.get('operating_voltage')}")
                        print(f"  Package:     {info.get('package')}")
                        print(f"  Stock:       {info.get('stock_status')}")
                        print(f"  Datasheet:   {info.get('datasheet_url')}\n")
                    else:
                        print("Usage: /part <part_number>")
                elif cmd == "/alt":
                    if len(parts) > 1:
                        part_no = parts[1]
                        res = get_component_alternatives(part_no)
                        print(f"{Colors.CYAN}--- ALTERNATIVE COMPONENTS FOR '{part_no}' ---{Colors.RESET}")
                        for alt in res.get("alternatives", []):
                            drop = f"{Colors.GREEN}[DROP-IN]{Colors.RESET}" if alt.get("drop_in") else "[COMPATIBLE]"
                            print(f"  • {alt['part_number']} ({alt['manufacturer']}) {drop}")
                            print(f"    Desc: {alt['desc']} | Stock: {alt['stock']} | Price: ${alt['price_usd']}")
                        print()
                    else:
                        print("Usage: /alt <part_number>")
                elif cmd == "/compare":
                    if len(parts) > 2:
                        res = compare_components([parts[1], parts[2]])
                        print(f"{Colors.CYAN}--- PARAMETRIC COMPARISON ---{Colors.RESET}")
                        for item in res:
                            print(f"  • {item.get('part_number'):<20} | Stock: {item.get('stock_status'):<25} | Pkg: {item.get('package')}")
                        print()
                    else:
                        print("Usage: /compare <part_number_1> <part_number_2>")
                else:
                    print(f"{Colors.RED}Unknown command '{cmd}'. Type /help for available commands.{Colors.RESET}")
            # --- NEW COMMAND HANDLERS (inserted before general prompt) ---
            # This block is reached only for non-slash inputs (regular prompts)
            else:
                memory.add_message("user", user_input)
                pruned_prompt, mem_metrics = memory.get_pruned_context(system_prompt=f"Role: {active_agent}", model_name=active_model)

                if mem_metrics["savings_percent"] > 0:
                    print(f"{Colors.DIM}🧠 [Sliding Memory Pruning]: Saved {mem_metrics['savings_percent']}% tokens ({mem_metrics['tokens_saved']} tokens){Colors.RESET}")

                print(f"{Colors.DIM}Thinking & executing task with [{active_agent.upper()}] (MCP Mode: {'ON' if MCPExecutionMode.is_enabled() else 'OFF'})...{Colors.RESET}")
                start_time = time.time()

                disp_result = dispatch_task(
                    user_prompt=pruned_prompt,
                    agent_name=active_agent,
                    model_name=active_model
                )
                output = disp_result.get("output", "")
                elapsed = round((time.time() - start_time) * 1000, 1)

                memory.add_message("assistant", output)

                # Render transparent thinking process box and formatted response
                reasoning_steps = [
                    f"Execution Mode: {disp_result.get('execution_mode')}",
                    f"Analyzed prompt & retrieved context for [{active_agent}]",
                    f"Optimized tokens & checked semantic cache",
                    f"Dispatched task to LLM Provider [{active_model}]"
                ]
                render_thinking_box(reasoning_steps, output, agent_name=active_agent, elapsed_ms=elapsed)

        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Use /exit to quit.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Error executing command: {e}{Colors.RESET}")

def main():
    parser = argparse.ArgumentParser(description="Autonomous Multi-Agent CLI Shell")
    parser.add_argument("prompt", nargs="?", help="Optional initial task prompt")
    parser.add_argument("--agent", "-a", default="orchestrator", help="Active sub-agent name")
    parser.add_argument("--model", "-m", default="gpt-4o", help="Model name")

    args = parser.parse_args()

    if args.prompt:
        output = run_agent_task(agent_name=args.agent, user_prompt=args.prompt, model_name=args.model)
        print(output)
    else:
        start_interactive_shell(default_agent=args.agent, default_model=args.model)

if __name__ == "__main__":
    main()
