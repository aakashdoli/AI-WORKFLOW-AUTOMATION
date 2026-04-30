import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models.schema import Base, Workflow, PipelineExecution, ProcessedResult, ExecutionStatus
from datetime import datetime

load_dotenv()

# Production DB URL (PostgreSQL)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/ai_ops")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

class DatabaseService:
    def __init__(self):
        self.db = SessionLocal()

    def create_workflow(self, name, description=""):
        workflow = Workflow(name=name, description=description)
        self.db.add(workflow)
        self.db.commit()
        self.db.refresh(workflow)
        return workflow

    def start_execution(self, workflow_id):
        execution = PipelineExecution(workflow_id=workflow_id, status=ExecutionStatus.RUNNING)
        self.db.add(execution)
        self.db.commit()
        self.db.refresh(execution)
        return execution

    def complete_execution(self, execution_id, latency_ms=0, token_usage=0, error=None):
        execution = self.db.query(PipelineExecution).filter(PipelineExecution.id == execution_id).first()
        if execution:
            execution.status = ExecutionStatus.FAILED if error else ExecutionStatus.COMPLETED
            execution.completed_at = datetime.utcnow()
            execution.latency_ms = latency_ms
            execution.token_usage = token_usage
            execution.error_message = error
            self.db.commit()
            self.db.refresh(execution)
        return execution

    def save_result(self, execution_id, input_data, output_data, category=None, priority=None, sentiment=None, confidence_score=None):
        result = ProcessedResult(
            execution_id=execution_id,
            input_data=input_data,
            output_data=output_data,
            category=category,
            priority=priority,
            sentiment=sentiment,
            confidence_score=confidence_score
        )
        self.db.add(result)
        self.db.commit()
        return result

    def get_all_workflows(self):
        return self.db.query(Workflow).all()

    def get_executions(self, workflow_id=None):
        query = self.db.query(PipelineExecution)
        if workflow_id:
            query = query.filter(PipelineExecution.workflow_id == workflow_id)
        return query.order_by(PipelineExecution.started_at.desc()).all()

    def get_results(self, execution_id):
        return self.db.query(ProcessedResult).filter(ProcessedResult.execution_id == execution_id).all()
    
    def close(self):
        self.db.close()
