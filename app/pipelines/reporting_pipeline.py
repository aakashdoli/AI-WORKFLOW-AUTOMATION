import pandas as pd
from typing import List
from app.services.llm_service import LLMService
from app.services.database_service import DatabaseService
from app.pipelines.classification_pipeline import ClassificationPipeline
from app.pipelines.fraud_pipeline import FraudPipeline
from app.pipelines.kpi_pipeline import KPIPipeline
from app.pipelines.summarization_pipeline import SummarizationPipeline
from app.utils.logger import logger
import json
import time
from datetime import datetime

class ReportingPipeline:
    def __init__(self, db_service: DatabaseService, llm_service: LLMService):
        self.db_service = db_service
        self.llm_service = llm_service
        self.classification_pipeline = ClassificationPipeline(llm_service)
        self.fraud_pipeline = FraudPipeline(llm_service)
        self.kpi_pipeline = KPIPipeline(llm_service)
        self.summarization_pipeline = SummarizationPipeline(llm_service)

    def run_workflow(self, workflow_name: str, csv_path: str):
        logger.info(f"Triggering workflow: {workflow_name} with file: {csv_path}")
        start_time = time.time()
        
        # 1. Initialize Database & Workflow
        workflows = self.db_service.get_all_workflows()
        workflow = next((w for w in workflows if w.name == workflow_name), None)
        if not workflow:
            workflow = self.db_service.create_workflow(workflow_name, f"Strategic Pipeline for {workflow_name}")
        
        execution = self.db_service.start_execution(workflow.id)
        total_tokens = 0
        
        try:
            # 2. Data Ingestion
            df = pd.read_csv(csv_path)
            records = df.to_dict(orient="records")
            
            # 3. Dynamic Workflow Routing & Processing
            if "Fraud" in workflow_name or "transaction" in csv_path.lower():
                from app.services.notification_service import NotificationService
                notifier = NotificationService()
                results, tokens = self.fraud_pipeline.analyze_transactions(records)
                total_tokens = tokens
                for res in results:
                    self.db_service.save_result(
                        execution_id=execution.id,
                        input_data=json.dumps(res.transaction_id),
                        output_data=res.reasoning,
                        category="Fraud Analysis",
                        priority=res.risk_level,
                        confidence_score=res.confidence_score
                    )
                    if res.risk_level == "High":
                        notifier.send_slack_alert(f"Critical Fraud Risk Detected! ID: {res.transaction_id}. Reasoning: {res.anomaly_explanation}", level="CRITICAL")
            
            elif "KPI" in workflow_name or "metric" in csv_path.lower():
                metrics_summary = df.describe().to_dict()
                report, tokens = self.kpi_pipeline.generate_report(metrics_summary)
                total_tokens = tokens
                self.db_service.save_result(
                    execution_id=execution.id,
                    input_data="Batch Metrics",
                    output_data=report.management_summary,
                    category="Executive KPI",
                    priority=report.strategic_priority
                )
            
            else:
                results, tokens = self.classification_pipeline.classify_records(records)
                total_tokens = tokens
                for res in results:
                    matching_record = next((r for r in records if str(r.get("Ticket ID") or r.get("id")) == res.ticket_id), {})
                    self.db_service.save_result(
                        execution_id=execution.id,
                        input_data=json.dumps(matching_record),
                        output_data=res.reasoning,
                        category=res.category,
                        priority=res.priority
                    )

            latency = int((time.time() - start_time) * 1000)
            self.db_service.complete_execution(execution.id, latency_ms=latency, token_usage=total_tokens)
            
            logger.info(f"Workflow {workflow_name} completed in {latency}ms using {total_tokens} tokens")
            return execution.id, "Workflow completed successfully."
            
        except Exception as e:
            logger.error(f"Workflow {workflow_name} failed: {e}")
            self.db_service.complete_execution(execution.id, error=str(e))
            raise e
