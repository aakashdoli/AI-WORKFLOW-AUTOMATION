from typing import List, Optional
from pydantic import BaseModel
from backend.services.llm_service import LLMService

class ClassificationResult(BaseModel):
    ticket_id: str
    category: str
    priority: str
    reasoning: str

class ClassificationPipeline:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def classify_records(self, records: List[dict]) -> tuple[List[ClassificationResult], int]:
        prompt = f"""
        Classify the following business records based on their descriptions.
        Categories: Billing Issue, Authentication, Refund Issue, Technical Issue, Escalation Required, Fraud Risk.
        Priorities: High, Medium, Low.
        
        Records:
        {records}
        
        Return a list of classification objects with ticket_id, category, priority, and a brief reasoning.
        """
        
        results, tokens = self.llm_service.get_structured_output(
            prompt=prompt,
            response_mime_type="backend.ication/json",
            response_schema=List[ClassificationResult]
        )
        return results, tokens
