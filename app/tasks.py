from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "ai_ops_tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task(bind=True)
def run_workflow_task(self, workflow_name: str, csv_path: str):
    from app.services.database_service import DatabaseService
    from app.services.llm_service import LLMService
    from app.pipelines.reporting_pipeline import ReportingPipeline
    
    db_service = DatabaseService()
    llm_service = LLMService()
    pipeline = ReportingPipeline(db_service, llm_service)
    
    try:
        exec_id, msg = pipeline.run_workflow(workflow_name, csv_path)
        return {"execution_id": exec_id, "status": "COMPLETED", "message": msg}
    except Exception as e:
        return {"status": "FAILED", "error": str(e)}
    finally:
        db_service.close()
