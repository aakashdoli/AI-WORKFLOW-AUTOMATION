from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum as SQLEnum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ExecutionStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Workflow(Base):
    __tablename__ = "workflows"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    executions = relationship("PipelineExecution", back_populates="workflow")

class PipelineExecution(Base):
    __tablename__ = "pipeline_executions"
    
    id = Column(Integer, primary_key=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"))
    status = Column(SQLEnum(ExecutionStatus), default=ExecutionStatus.PENDING)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    error_message = Column(Text)
    
    workflow = relationship("Workflow", back_populates="executions")
    results = relationship("ProcessedResult", back_populates="execution")

class ProcessedResult(Base):
    __tablename__ = "processed_results"
    
    id = Column(Integer, primary_key=True)
    execution_id = Column(Integer, ForeignKey("pipeline_executions.id"))
    input_data = Column(Text)  # JSON or CSV snippet
    output_data = Column(Text)  # JSON or summary
    category = Column(String(50))  # For classification results
    priority = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    execution = relationship("PipelineExecution", back_populates="results")
