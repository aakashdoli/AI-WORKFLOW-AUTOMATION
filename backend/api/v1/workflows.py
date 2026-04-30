from fastapi import APIRouter, Depends, HTTPException
from typing import List
from backend.services.database_service import DatabaseService
from backend.schemas.workflow import WorkflowSchema, WorkflowExecuteRequest, ExecutionResponse
from backend.workers.tasks import run_workflow_task
import os

router = APIRouter(prefix="/workflows", tags=["Workflows"])

@router.get("/", response_model=List[WorkflowSchema])
def get_workflows():
    db = DatabaseService()
    workflows = db.get_all_workflows()
    return workflows

@router.post("/execute", response_model=ExecutionResponse)
async def execute_workflow(request: WorkflowExecuteRequest):
    if not os.path.exists(request.csv_path):
        raise HTTPException(status_code=404, detail="CSV file not found")
    
    task = run_workflow_task.delay(request.workflow_name, request.csv_path)
    
    return ExecutionResponse(
        execution_id=0,
        status="ACCEPTED",
        message=f"Workflow queued. Task ID: {task.id}"
    )
