from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.database_service import DatabaseService, init_db
from app.services.llm_service import LLMService
from app.pipelines.reporting_pipeline import ReportingPipeline
import os

app = FastAPI(title="AI Ops Automation Platform API")

# Initialize DB on startup
@app.on_event("startup")
def startup():
    init_db()

class WorkflowRequest(BaseModel):
    workflow_name: str
    csv_path: str

class ExecutionResponse(BaseModel):
    execution_id: int
    status: str
    message: str

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/workflows/execute", response_model=ExecutionResponse)
async def execute_workflow(request: WorkflowRequest):
    from app.tasks import run_workflow_task
    
    if not os.path.exists(request.csv_path):
        raise HTTPException(status_code=404, detail="CSV file not found")
    
    task = run_workflow_task.delay(request.workflow_name, request.csv_path)
    
    return ExecutionResponse(
        execution_id=0, 
        status="ACCEPTED",
        message=f"Workflow queued with Task ID: {task.id}"
    )

@app.get("/workflows/history")
def get_history():
    db_service = DatabaseService()
    executions = db_service.get_executions()
    return [{"id": e.id, "workflow": e.workflow.name, "status": e.status, "latency": e.latency_ms} for e in executions]

@app.get("/system/metrics")
def get_metrics():
    db_service = DatabaseService()
    executions = db_service.get_executions()
    total = len(executions)
    success = len([e for e in executions if e.status == "COMPLETED"])
    tokens = sum([e.token_usage for e in executions if e.token_usage])
    
    return {
        "total_executions": total,
        "success_rate": (success / total * 100) if total > 0 else 0,
        "total_tokens": tokens,
        "active_workers": 4 # Simulated for enterprise feel
    }

@app.get("/analytics/usage")
def get_usage_analytics():
    db_service = DatabaseService()
    # Simple aggregation logic
    executions = db_service.get_executions()
    usage = {}
    for e in executions:
        usage[e.workflow.name] = usage.get(e.workflow.name, 0) + 1
    return usage
