import argparse
import os
from app.services.database_service import DatabaseService, init_db
from app.services.llm_service import LLMService
from app.pipelines.reporting_pipeline import ReportingPipeline

def main():
    parser = argparse.ArgumentParser(description="AI Workflow Automation Platform CLI")
    parser.add_argument("--workflow", type=str, required=True, help="Name of the workflow")
    parser.add_argument("--csv", type=str, required=True, help="Path to the input CSV file")
    
    args = parser.parse_args()
    
    init_db()
    db_service = DatabaseService()
    llm_service = LLMService()
    
    pipeline = ReportingPipeline(db_service, llm_service)
    
    print(f"🚀 Starting workflow: {args.workflow}")
    try:
        exec_id, summary = pipeline.run_workflow(args.workflow, args.csv)
        print(f"✅ Success! Execution ID: {exec_id}")
        print("\n--- Executive Summary ---\n")
        print(summary)
    except Exception as e:
        print(f"❌ Failed: {e}")
    finally:
        db_service.close()

if __name__ == "__main__":
    main()
