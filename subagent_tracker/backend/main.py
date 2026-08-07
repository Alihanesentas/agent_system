import os
import csv
import io
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime

from subagent_tracker.backend.database import init_db, AgentLog, BenchmarkSession, db
from subagent_tracker.backend.tracker import process_agent_activity, MODEL_PRICING
from core.cache import get_cache_metrics

app = FastAPI(
    title="Subagent Token Tracer API",
    description="Real-time token usage, latency, and cost tracking system for multi-agent workflows.",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

# --- Schemas ---

class LogPayload(BaseModel):
    agent_name: str
    model_name: str = "gpt-4o"
    input_text: str
    output_text: str
    execution_time_ms: Optional[float] = 0.0
    session_id: Optional[int] = None
    status: Optional[str] = "success"

class SessionCreatePayload(BaseModel):
    name: str
    description: Optional[str] = ""
    version_tag: Optional[str] = "v1.0"

# --- Endpoints ---

@app.post("/api/log")
def create_log(payload: LogPayload):
    """Ingests agent activity, calculates tokens and estimated cost, and stores trace log."""
    try:
        p_tokens, c_tokens, t_tokens, cost = process_agent_activity(
            input_text=payload.input_text,
            output_text=payload.output_text,
            model_name=payload.model_name
        )

        session_obj = None
        if payload.session_id:
            session_obj = BenchmarkSession.get_or_none(BenchmarkSession.id == payload.session_id)

        log_entry = AgentLog.create(
            agent_name=payload.agent_name,
            model_name=payload.model_name,
            input_text=payload.input_text,
            output_text=payload.output_text,
            prompt_tokens=p_tokens,
            completion_tokens=c_tokens,
            total_tokens=t_tokens,
            estimated_cost_usd=cost,
            execution_time_ms=payload.execution_time_ms or 0.0,
            status=payload.status or "success",
            session=session_obj,
            created_at=datetime.now()
        )

        return {
            "status": "success",
            "log_id": log_entry.id,
            "prompt_tokens": p_tokens,
            "completion_tokens": c_tokens,
            "total_tokens": t_tokens,
            "estimated_cost_usd": cost,
            "execution_time_ms": payload.execution_time_ms
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to log agent activity: {str(e)}")

@app.get("/api/logs")
def get_logs(
    agent_name: Optional[str] = None,
    session_id: Optional[int] = None,
    limit: int = Query(50, ge=1, le=10000),
    offset: int = Query(0, ge=0)
):
    """Returns paginated logs with optional filtering by agent name or benchmark session."""
    query = AgentLog.select().order_by(AgentLog.created_at.desc())

    if agent_name:
        query = query.where(AgentLog.agent_name == agent_name)
    if session_id:
        query = query.where(AgentLog.session == session_id)

    total_count = query.count()
    logs = list(query.offset(offset).limit(limit).dicts())

    return {
        "total": total_count,
        "offset": offset,
        "limit": limit,
        "logs": logs
    }

@app.get("/api/stats")
def get_stats():
    """Aggregates system-wide analytics, agent breakdown, model usage, and cost summary."""
    logs = list(AgentLog.select().dicts())

    if not logs:
        return {
            "total_calls": 0,
            "total_tokens": 0,
            "total_prompt_tokens": 0,
            "total_completion_tokens": 0,
            "total_cost_usd": 0.0,
            "avg_latency_ms": 0.0,
            "by_agent": {},
            "by_model": {}
        }

    total_calls = len(logs)
    total_tokens = sum(l["total_tokens"] for l in logs)
    total_prompt_tokens = sum(l["prompt_tokens"] for l in logs)
    total_completion_tokens = sum(l["completion_tokens"] for l in logs)
    total_cost_usd = round(sum(l["estimated_cost_usd"] for l in logs), 6)
    avg_latency_ms = round(sum(l["execution_time_ms"] for l in logs) / total_calls, 2)

    by_agent: Dict[str, Dict[str, Any]] = {}
    by_model: Dict[str, Dict[str, Any]] = {}

    for l in logs:
        agent = l["agent_name"]
        model = l["model_name"]

        # Aggregate by agent
        if agent not in by_agent:
            by_agent[agent] = {"calls": 0, "total_tokens": 0, "cost_usd": 0.0, "avg_latency_ms": 0.0}
        by_agent[agent]["calls"] += 1
        by_agent[agent]["total_tokens"] += l["total_tokens"]
        by_agent[agent]["cost_usd"] = round(by_agent[agent]["cost_usd"] + l["estimated_cost_usd"], 6)
        by_agent[agent]["avg_latency_ms"] += l["execution_time_ms"]

        # Aggregate by model
        if model not in by_model:
            by_model[model] = {"calls": 0, "total_tokens": 0, "cost_usd": 0.0}
        by_model[model]["calls"] += 1
        by_model[model]["total_tokens"] += l["total_tokens"]
        by_model[model]["cost_usd"] = round(by_model[model]["cost_usd"] + l["estimated_cost_usd"], 6)

    # Average latencies
    for agent in by_agent:
        by_agent[agent]["avg_latency_ms"] = round(by_agent[agent]["avg_latency_ms"] / by_agent[agent]["calls"], 2)

    return {
        "total_calls": total_calls,
        "total_tokens": total_tokens,
        "total_prompt_tokens": total_prompt_tokens,
        "total_completion_tokens": total_completion_tokens,
        "total_cost_usd": total_cost_usd,
        "avg_latency_ms": avg_latency_ms,
        "by_agent": by_agent,
        "by_model": by_model
    }

@app.get("/api/cache/stats")
def cache_stats():
    """Retrieves semantic cache performance metrics."""
    return get_cache_metrics()

@app.get("/api/export/csv")
def export_csv(
    agent_name: Optional[str] = None,
    session_id: Optional[int] = None
):
    """Exports trace activity logs to CSV format."""
    query = AgentLog.select().order_by(AgentLog.created_at.desc())

    if agent_name:
        query = query.where(AgentLog.agent_name == agent_name)
    if session_id:
        query = query.where(AgentLog.session == session_id)

    logs = list(query.dicts())

    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        "ID", "Created At", "Agent Name", "Model Name", 
        "Prompt Tokens", "Completion Tokens", "Total Tokens", 
        "Estimated Cost (USD)", "Latency (ms)", "Status", 
        "Input Text", "Output Text"
    ])

    for l in logs:
        writer.writerow([
            l["id"],
            l["created_at"].strftime("%Y-%m-%d %H:%M:%S") if isinstance(l["created_at"], datetime) else str(l["created_at"]),
            l["agent_name"],
            l["model_name"],
            l["prompt_tokens"],
            l["completion_tokens"],
            l["total_tokens"],
            l["estimated_cost_usd"],
            l["execution_time_ms"],
            l["status"],
            l["input_text"],
            l["output_text"]
        ])

    csv_content = output.getvalue()
    filename = f"token_trace_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.post("/api/sessions")
def create_session(payload: SessionCreatePayload):
    """Creates a new benchmark session to group agent execution iterations."""
    session = BenchmarkSession.create(
        name=payload.name,
        description=payload.description or "",
        version_tag=payload.version_tag or "v1.0",
        created_at=datetime.now()
    )
    return {
        "status": "success",
        "session_id": session.id,
        "name": session.name,
        "version_tag": session.version_tag
    }

@app.get("/api/sessions")
def get_sessions():
    """Retrieves all benchmark sessions with aggregated tokens, cost, and efficiency comparisons."""
    sessions = list(BenchmarkSession.select().order_by(BenchmarkSession.created_at.desc()).dicts())

    result = []
    for s in sessions:
        logs = list(AgentLog.select().where(AgentLog.session == s["id"]).dicts())
        t_tokens = sum(l["total_tokens"] for l in logs)
        t_cost = round(sum(l["estimated_cost_usd"] for l in logs), 6)
        avg_lat = round(sum(l["execution_time_ms"] for l in logs) / len(logs), 2) if logs else 0.0
        
        s["total_calls"] = len(logs)
        s["total_tokens"] = t_tokens
        s["total_cost_usd"] = t_cost
        s["avg_latency_ms"] = avg_lat
        result.append(s)

    return result

@app.delete("/api/logs/clear")
def clear_logs():
    """Resets logs for benchmarking clean state."""
    AgentLog.delete().execute()
    return {"status": "success", "message": "All activity logs have been cleared."}

# --- REST API Gateway for External Apps & IDEs ---

class TaskPayload(BaseModel):
    prompt: str
    agent_name: Optional[str] = "orchestrator"
    model_name: Optional[str] = "gpt-4o"

@app.post("/api/v1/agent/run")
def api_run_agent(payload: TaskPayload):
    """Triggers an agent task remotely via REST API."""
    from core.runner import run_agent_task
    output = run_agent_task(agent_name=payload.agent_name or "orchestrator", user_prompt=payload.prompt, model_name=payload.model_name or "gpt-4o")
    return {"status": "success", "agent": payload.agent_name, "model": payload.model_name, "output": output}

@app.post("/api/v1/consensus")
def api_consensus(payload: TaskPayload):
    """Triggers Multi-Model Consensus Voting remotely."""
    from core.consensus import run_consensus
    return run_consensus(payload.prompt)

@app.get("/api/v1/pinout")
def api_pinout(sda: str = "GPIO21", scl: str = "GPIO22", output_pin: str = "GPIO34"):
    """Checks GPIO pin conflicts remotely via REST API."""
    from core.pinout import check_pinout_conflicts
    return check_pinout_conflicts({"I2C_SDA": sda, "I2C_SCL": scl, "OUTPUT_PIN": output_pin}, mcu_family="ESP32")

