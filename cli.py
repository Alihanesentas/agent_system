#!/usr/bin/env python3
"""
Cross-Platform Multi-Agent Token Tracer CLI
Compatible with Linux, macOS, and Windows terminals.
"""

import sys
import os
import time
import argparse
import csv
import json
import urllib.request
import urllib.error
from datetime import datetime

API_BASE = "http://127.0.0.1:8000/api"

# ANSI Color Codes for Terminal Output (supported across modern Windows Terminal, macOS, and Linux)
class Colors:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

    @staticmethod
    def supports_color():
        return sys.stdout.isatty() and (os.name != 'nt' or 'ANSICON' in os.environ or 'WT_SESSION' in os.environ or 'TERM' in os.environ)

def colorize(text, color):
    if Colors.supports_color():
        return f"{color}{text}{Colors.RESET}"
    return text

def fetch_json(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'TracerCLI/1.0'})
        with urllib.request.urlopen(req, timeout=4) as res:
            return json.loads(res.read().decode('utf-8'))
    except Exception as e:
        print(colorize(f"⚠️ Error connecting to Tracker API ({url}): {e}", Colors.RED))
        sys.exit(1)

def print_banner():
    banner = f"""
{colorize('====================================================', Colors.CYAN)}
{colorize('  ⚡ MULTI-AGENT TOKEN TRACER CLI ', Colors.BOLD + Colors.GREEN)}
{colorize('====================================================', Colors.CYAN)}
"""
    print(banner)

def cmd_stats(args):
    data = fetch_json(f"{API_BASE}/stats")
    print_banner()
    
    print(colorize("📊 GLOBAL SUMMARY METRICS", Colors.BOLD + Colors.CYAN))
    print(f"  • Total Agent Calls:    {colorize(str(data['total_calls']), Colors.BOLD)}")
    print(f"  • Total Tokens:         {colorize(str(data['total_tokens']), Colors.GREEN)} (Prompt: {data['total_prompt_tokens']}, Completion: {data['total_completion_tokens']})")
    print(f"  • Estimated Total Cost: {colorize('$' + str(round(data['total_cost_usd'], 6)), Colors.YELLOW)}")
    print(f"  • Avg Latency:          {colorize(str(data['avg_latency_ms']) + ' ms', Colors.CYAN)}")
    print("-" * 52)

    print(colorize("\n🤖 BREAKDOWN BY AGENT", Colors.BOLD + Colors.CYAN))
    if not data.get("by_agent"):
        print("  (No agent telemetry recorded yet)")
    else:
        print(f"{'AGENT':<16} | {'CALLS':<6} | {'TOKENS':<8} | {'COST ($)':<10} | {'LATENCY (ms)'}")
        print("-" * 52)
        for agent, d in data["by_agent"].items():
            print(f"{colorize(agent.upper(), Colors.BOLD):<24} | {d['calls']:<6} | {d['total_tokens']:<8} | ${d['cost_usd']:<9.5f} | {d['avg_latency_ms']} ms")

    print(colorize("\n⚡ BREAKDOWN BY MODEL", Colors.BOLD + Colors.CYAN))
    if not data.get("by_model"):
        print("  (No model telemetry recorded yet)")
    else:
        print(f"{'MODEL':<20} | {'CALLS':<6} | {'TOKENS':<8} | {'COST ($)'}")
        print("-" * 52)
        for model, d in data["by_model"].items():
            print(f"{model:<20} | {d['calls']:<6} | {d['total_tokens']:<8} | ${d['cost_usd']:.5f}")
    print()

def cmd_logs(args):
    url = f"{API_BASE}/logs?limit={args.limit}"
    if args.agent:
        url += f"&agent_name={args.agent}"
    
    res = fetch_json(url)
    logs = res.get("logs", [])

    print_banner()
    print(colorize(f"📜 RECENT ACTIVITY LOGS (Top {len(logs)})", Colors.BOLD + Colors.CYAN))
    print("-" * 78)
    print(f"{'ID':<4} | {'TIMESTAMP':<19} | {'AGENT':<12} | {'MODEL':<14} | {'TOKENS':<8} | {'COST ($)':<8} | {'LATENCY'}")
    print("-" * 78)

    for l in logs:
        ts = str(l['created_at'])[:19]
        agent = l['agent_name']
        model = l['model_name']
        tokens = l['total_tokens']
        cost = f"${l['estimated_cost_usd']:.5f}"
        lat = f"{l['execution_time_ms']} ms"
        print(f"{l['id']:<4} | {ts:<19} | {colorize(agent, Colors.GREEN):<21} | {model:<14} | {tokens:<8} | {cost:<8} | {lat}")
    print()

def cmd_watch(args):
    interval = args.interval
    print(colorize(f"👀 Live Terminal Monitoring Mode (Refresh every {interval}s)... Press Ctrl+C to exit.", Colors.YELLOW))
    time.sleep(1)
    
    try:
        while True:
            # Clear terminal screen (cross-platform)
            os.system('cls' if os.name == 'nt' else 'clear')
            cmd_stats(args)
            print(colorize(f"🔄 Auto-refreshing... (Interval: {interval}s) | Ctrl+C to stop", Colors.DIM))
            time.sleep(interval)
    except KeyboardInterrupt:
        print(colorize("\nStopped monitoring.", Colors.YELLOW))

def cmd_export(args):
    print(colorize("📥 Exporting trace logs to CSV...", Colors.CYAN))
    url = f"{API_BASE}/logs?limit=500"
    if args.agent:
        url += f"&agent_name={args.agent}"
    
    res = fetch_json(url)
    logs = res.get("logs", [])

    # Filter dates if provided
    if args.start:
        logs = [l for l in logs if str(l['created_at'])[:10] >= args.start]
    if args.end:
        logs = [l for l in logs if str(l['created_at'])[:10] <= args.end]

    output_filename = args.output or f"token_trace_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(output_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "ID", "Created At", "Agent Name", "Model Name", 
            "Prompt Tokens", "Completion Tokens", "Total Tokens", 
            "Estimated Cost (USD)", "Latency (ms)", "Status", 
            "Input Text", "Output Text"
        ])

        for l in logs:
            writer.writerow([
                l["id"], l["created_at"], l["agent_name"], l["model_name"],
                l["prompt_tokens"], l["completion_tokens"], l["total_tokens"],
                l["estimated_cost_usd"], l["execution_time_ms"], l["status"],
                l["input_text"], l["output_text"]
            ])

    print(colorize(f"✅ Successfully exported {len(logs)} records to '{output_filename}'", Colors.BOLD + Colors.GREEN))

def cmd_test(args):
    print(colorize("⚡ Running test multi-agent workflow sequence from terminal...", Colors.YELLOW))
    try:
        from core.runner import run_agent_task
        run_agent_task("orchestrator", "Terminal CLI test orchestrator workflow", "gpt-4o")
        run_agent_task("planner", "Break down CLI CSV exporter into streaming chunks", "gpt-4o")
        run_agent_task("software", "Write python csv writer utility function", "gpt-4o-mini")
        run_agent_task("tutor", "Explain terminal ANSI color escape codes", "gemini-1.5-flash")
        print(colorize("✅ Multi-agent execution completed! Logged to tracker backend.", Colors.BOLD + Colors.GREEN))
    except Exception as e:
        print(colorize(f"⚠️ Error running test: {e}", Colors.RED))

def main():
    parser = argparse.ArgumentParser(
        description="Multi-Agent Token Tracer Cross-Platform CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Stats command
    p_stats = subparsers.add_parser("stats", help="Display global token, cost, and agent statistics")

    # Logs command
    p_logs = subparsers.add_parser("logs", help="View recent activity trace logs")
    p_logs.add_argument("--agent", help="Filter logs by agent name")
    p_logs.add_argument("--limit", type=int, default=20, help="Number of logs to display (default: 20)")

    # Watch command
    p_watch = subparsers.add_parser("watch", help="Live terminal monitoring mode")
    p_watch.add_argument("--interval", type=int, default=3, help="Refresh interval in seconds (default: 3)")

    # Export command
    p_export = subparsers.add_parser("export", help="Export trace logs to CSV file")
    p_export.add_argument("--output", help="Output CSV filename (default: token_trace_YYYYMMDD_HHMMSS.csv)")
    p_export.add_argument("--agent", help="Filter by agent name")
    p_export.add_argument("--start", help="Filter start date (YYYY-MM-DD)")
    p_export.add_argument("--end", help="Filter end date (YYYY-MM-DD)")

    # Test command
    p_test = subparsers.add_parser("test", help="Execute a sample multi-agent test sequence")

    args = parser.parse_args()

    if args.command == "stats":
        cmd_stats(args)
    elif args.command == "logs":
        cmd_logs(args)
    elif args.command == "watch":
        cmd_watch(args)
    elif args.command == "export":
        cmd_export(args)
    elif args.command == "test":
        cmd_test(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
