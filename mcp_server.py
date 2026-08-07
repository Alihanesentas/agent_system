#!/usr/bin/env python3
"""
Standard Model Context Protocol (MCP) Server for Agent System.
Exposes multidisciplinary engineering tools (Electronics, Software, CAD, Research, RAG, Unit Testing)
to Claude Desktop, Cursor, VSCode, and Antigravity via standard JSON-RPC 2.0 Stdio protocol.
"""

import sys
import json
import os
from typing import Dict, Any, List

# Core tool handlers
from core.runner import run_agent_task
from core.rag import search as rag_search, index_file, get_index_stats
from core.schematics import parse_kicad_schematic, parse_bom_csv
from core.component_search import search_component, get_component_alternatives
from core.pinout import check_pinout_conflicts
from core.consensus import run_consensus
from core.mechanical import generate_openscad_enclosure, recommend_slicer_settings
from core.research import search_arxiv_papers, generate_patent_prior_art_query
from core.agent_test import create_system_test_suite
from core.executor import execute_command

MCP_TOOLS = [
    {
        "name": "agent_run_task",
        "description": "Executes a multidisciplinary agent task (software, electronics, planner, reviewer, tutor)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "Instructions for the agent"},
                "agent_name": {"type": "string", "enum": ["orchestrator", "planner", "software", "electronics", "reviewer", "tutor"], "default": "orchestrator"},
                "model_name": {"type": "string", "default": "gpt-4o"}
            },
            "required": ["prompt"]
        }
    },
    {
        "name": "rag_search",
        "description": "Performs semantic search across indexed PDF datasheets, C/C++ code, and project docs",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query text"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "search_component",
        "description": "Searches Mouser/DigiKey/LCSC component API for stock, pricing, and specs",
        "inputSchema": {
            "type": "object",
            "properties": {
                "part_number": {"type": "string", "description": "Manufacturer part number e.g. ESP32-WROOM-32E"}
            },
            "required": ["part_number"]
        }
    },
    {
        "name": "check_pinout",
        "description": "Audits GPIO pin assignments for ESP32/STM32 pin collisions and strapping hazards",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sda_pin": {"type": "string", "default": "GPIO21"},
                "scl_pin": {"type": "string", "default": "GPIO22"},
                "output_pin": {"type": "string", "default": "GPIO34"}
            },
            "required": ["sda_pin", "scl_pin", "output_pin"]
        }
    },
    {
        "name": "generate_3d_enclosure",
        "description": "Generates OpenSCAD 3D parametric enclosure script for electronic PCBs",
        "inputSchema": {
            "type": "object",
            "properties": {
                "length_mm": {"type": "number"},
                "width_mm": {"type": "number"},
                "height_mm": {"type": "number"}
            },
            "required": ["length_mm", "width_mm", "height_mm"]
        }
    },
    {
        "name": "search_academic_papers",
        "description": "Searches arXiv scientific preprints for R&D research literature",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Research topic query"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "run_consensus_voting",
        "description": "Runs parallel consensus voting across OpenAI, Claude, and Gemini models",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "Decision prompt to vote on"}
            },
            "required": ["prompt"]
        }
    }
]

def handle_mcp_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Handles standard JSON-RPC 2.0 MCP messages over Stdio."""
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "AgentSystemMCPServer", "version": "2.5.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": MCP_TOOLS}
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        try:
            if tool_name == "agent_run_task":
                out = run_agent_task(agent_name=args.get("agent_name", "orchestrator"), user_prompt=args["prompt"], model_name=args.get("model_name", "gpt-4o"))
                res_text = out
            elif tool_name == "rag_search":
                hits = rag_search(args["query"])
                res_text = json.dumps(hits, indent=2)
            elif tool_name == "search_component":
                info = search_component(args["part_number"])
                res_text = json.dumps(info, indent=2)
            elif tool_name == "check_pinout":
                assigns = {"I2C_SDA": args["sda_pin"], "I2C_SCL": args["scl_pin"], "OUTPUT": args["output_pin"]}
                info = check_pinout_conflicts(assigns)
                res_text = json.dumps(info, indent=2)
            elif tool_name == "generate_3d_enclosure":
                res_text = generate_openscad_enclosure(args["length_mm"], args["width_mm"], args["height_mm"])
            elif tool_name == "search_academic_papers":
                papers = search_arxiv_papers(args["query"])
                res_text = json.dumps(papers, indent=2)
            elif tool_name == "run_consensus_voting":
                c_res = run_consensus(args["prompt"])
                res_text = c_res.get("consensus_synthesis", "")
            else:
                res_text = f"Tool '{tool_name}' not found."

            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": res_text}]}
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32603, "message": str(e)}
            }
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method '{method}' not found."}
        }

def main():
    """Stdio listener loop for JSON-RPC 2.0 MCP Protocol."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_mcp_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"Parse error: {e}"}}
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
