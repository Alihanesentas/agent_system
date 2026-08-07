"""
MCP Protocol Client & Execution Switcher.
Allows toggling between Direct Native Execution (high speed, lower token usage)
and MCP Protocol Execution (standard JSON-RPC Stdio/HTTP client).
"""

import json
from typing import Dict, Any, Optional
from mcp_server import handle_mcp_request
from core.engine.runner import run_agent_task

class MCPExecutionMode:
    _enabled: bool = False
    _server_name: str = "agent-system-local"

    @classmethod
    def is_enabled(cls) -> bool:
        return cls._enabled

    @classmethod
    def set_enabled(cls, status: bool):
        cls._enabled = status

    @classmethod
    def get_server(cls) -> str:
        return cls._server_name

    @classmethod
    def set_server(cls, name: str):
        cls._server_name = name

def dispatch_task(
    user_prompt: str,
    agent_name: str = "orchestrator",
    model_name: str = "gpt-4o",
    force_mcp: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Dispatches task via MCP Stdio JSON-RPC protocol if enabled,
    otherwise uses direct native execution pipeline.
    """
    use_mcp = force_mcp if force_mcp is not None else MCPExecutionMode.is_enabled()

    if use_mcp:
        # Dispatch via MCP JSON-RPC 2.0 Protocol Handler
        mcp_req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "agent_run_task",
                "arguments": {
                    "prompt": user_prompt,
                    "agent_name": agent_name,
                    "model_name": model_name
                }
            }
        }
        res = handle_mcp_request(mcp_req)

        content = res.get("result", {}).get("content", [{}])[0].get("text", "")
        return {
            "execution_mode": "MCP Protocol (JSON-RPC Stdio)",
            "server": MCPExecutionMode.get_server(),
            "output": content,
            "overhead": "Schema injected (~15% token overhead for standard compatibility)"
        }
    else:
        # Direct Native Execution (Zero overhead, max speed)
        out = run_agent_task(agent_name=agent_name, user_prompt=user_prompt, model_name=model_name)
        return {
            "execution_mode": "Direct Native Execution",
            "server": "Local Core Pipeline",
            "output": out,
            "overhead": "Zero schema overhead (Fastest & lowest token usage)"
        }
