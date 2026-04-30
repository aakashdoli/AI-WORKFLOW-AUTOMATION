from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class WorkflowSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class WorkflowExecuteRequest(BaseModel):
    workflow_name: str
    csv_path: str

class ExecutionResponse(BaseModel):
    execution_id: int
    status: str
    message: str
