from fastapi import APIRouter
from typing import List, Dict
from backend.services.database_service import DatabaseService

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/overview")
def get_analytics_overview():
    db = DatabaseService()
    executions = db.get_executions()
    
    total = len(executions)
    success = len([e for e in executions if e.status == "COMPLETED"])
    tokens = sum([e.token_usage for e in executions if e.token_usage])
    
    # Calculate daily volume
    daily_volume = {}
    for e in executions:
        day = e.started_at.date().isoformat()
        daily_volume[day] = daily_volume.get(day, 0) + 1
        
    return {
        "total_executions": total,
        "success_rate": (success / total * 100) if total > 0 else 0,
        "total_tokens": tokens,
        "daily_volume": daily_volume
    }

@router.get("/workflows")
def get_workflow_distribution():
    db = DatabaseService()
    executions = db.get_executions()
    dist = {}
    for e in executions:
        name = e.workflow.name
        dist[name] = dist.get(name, 0) + 1
    return dist
