import pandas as pd
from typing import List
from app.services.llm_service import LLMService
from app.services.database_service import DatabaseService
from app.pipelines.classification_pipeline import ClassificationPipeline
from app.pipelines.summarization_pipeline import SummarizationPipeline
import json

class ReportingPipeline:
    def __init__(self, db_service: DatabaseService, llm_service: LLMService):
        self.db_service = db_service
        self.llm_service = llm_service
        self.classification_pipeline = ClassificationPipeline(llm_service)
        self.summarization_pipeline = SummarizationPipeline(llm_service)

    def run_workflow(self, workflow_name: str, csv_path: str):
        # 1. Initialize Database & Workflow
        workflows = self.db_service.get_all_workflows()
        workflow = next((w for w in workflows if w.name == workflow_name), None)
        if not workflow:
            workflow = self.db_service.create_workflow(workflow_name, f"Pipeline for {workflow_name}")
        
        execution = self.db_service.start_execution(workflow.id)
        
        try:
            # 2. Data Ingestion
            df = pd.read_csv(csv_path)
            records = df.to_dict(orient="records")
            
            # 3. AI Classification
            classification_results = self.classification_pipeline.classify_records(records)
            
            # 4. AI Summarization
            data_context = df.to_string() + "\n\nClassification Results:\n" + str([r.dict() for r in classification_results])
            executive_summary = self.summarization_pipeline.generate_executive_summary(data_context)
            
            # 5. Save Results
            for res in classification_results:
                # Find matching record to get input data
                matching_record = next((r for r in records if str(r.get("Ticket ID") or r.get("id")) == res.ticket_id), {})
                self.db_service.save_result(
                    execution_id=execution.id,
                    input_data=json.dumps(matching_record),
                    output_data=res.reasoning,
                    category=res.category,
                    priority=res.priority
                )
            
            # Save the executive summary as a final result or in a specific field (here as a general result)
            self.db_service.save_result(
                execution_id=execution.id,
                input_data="Full Batch",
                output_data=executive_summary,
                category="Executive Summary"
            )
            
            self.db_service.complete_execution(execution.id)
            return execution.id, executive_summary
            
        except Exception as e:
            self.db_service.complete_execution(execution.id, error=str(e))
            raise e
