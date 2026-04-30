import sys
import os
import random
from datetime import datetime, timedelta
import json

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.services.database_service import DatabaseService, init_db
from backend.models.schema import Workflow, PipelineExecution, ProcessedResult, ExecutionStatus

def seed_data():
    print("🚀 Initializing Enterprise AI Ops Demo Data Seeding...")
    init_db()
    db = DatabaseService()
    
    # 1. Ensure Workflows exist
    workflow_templates = [
        {"name": "Customer Support Ticket Automation", "description": "Automated ticket classification, priority prediction, and sentiment analysis."},
        {"name": "Financial Fraud Risk Analysis", "description": "Transaction anomaly detection and risk scoring for financial records."},
        {"name": "Executive KPI Intelligence", "description": "Summarization of operational metrics and strategic recommendation generation."},
        {"name": "Document Intelligence Workflow", "description": "Contract risk extraction and action item generation from legal documents."}
    ]
    
    workflows = []
    for template in workflow_templates:
        w = db.db.query(Workflow).filter(Workflow.name == template["name"]).first()
        if not w:
            w = db.create_workflow(template["name"], template["description"])
        workflows.append(w)

    # 2. Generate 150+ Executions
    print(f"📈 Generating 150 realistic executions across {len(workflows)} workflows...")
    
    start_date = datetime.now() - timedelta(days=30)
    
    for i in range(150):
        w = random.choice(workflows)
        status = random.choices(
            [ExecutionStatus.COMPLETED, ExecutionStatus.FAILED], 
            weights=[95, 5]
        )[0]
        
        latency = random.randint(300, 1200) if status == ExecutionStatus.COMPLETED else random.randint(50, 200)
        tokens = random.randint(800, 4500) if status == ExecutionStatus.COMPLETED else 0
        
        started_at = start_date + timedelta(
            days=random.randint(0, 29), 
            hours=random.randint(0, 23), 
            minutes=random.randint(0, 59)
        )
        
        execution = PipelineExecution(
            workflow_id=w.id,
            status=status,
            started_at=started_at,
            completed_at=started_at + timedelta(milliseconds=latency),
            latency_ms=latency,
            token_usage=tokens,
            error_message="API Timeout" if status == ExecutionStatus.FAILED else None
        )
        db.db.add(execution)
        db.db.flush()
        
        if status == ExecutionStatus.COMPLETED:
            category = random.choice(["Refund", "Technical", "Billing", "Fraud", "Strategic"])
            priority = random.choice(["High", "Medium", "Low"])
            
            result = ProcessedResult(
                execution_id=execution.id,
                input_data=json.dumps({"id": f"REC-{i}", "source": "Batch Pipeline"}),
                output_data=f"AI processing finalized for {w.name}.",
                category=category,
                priority=priority,
                confidence_score=random.randint(85, 99)
            )
            db.db.add(result)

    db.db.commit()
    print("✅ Seed data populated.")
    db.close()

if __name__ == "__main__":
    seed_data()
