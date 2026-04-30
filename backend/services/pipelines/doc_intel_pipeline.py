from typing import List, Optional
from pydantic import BaseModel
from backend.services.llm_service import LLMService
from backend.utils.logger import logger

class DocAnalysisResult(BaseModel):
    document_id: str
    summary: str
    risk_level: str # Critical, Significant, Minimal
    risk_explanation: str
    action_items: List[str]

class DocumentIntelPipeline:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def analyze_documents(self, documents: List[dict]) -> tuple[List[DocAnalysisResult], int]:
        logger.info(f"Starting Document Intelligence analysis for {len(documents)} docs")
        
        prompt = f"""
        Analyze the following document contents (legal/business/operational).
        Extract key risks and action items.
        
        Documents:
        {documents}
        
        For each document, provide:
        1. document_id
        2. summary (1-2 sentences)
        3. risk_level (Critical, Significant, Minimal)
        4. risk_explanation
        5. action_items (List of strings)
        """
        
        try:
            results, tokens = self.llm_service.get_structured_output(
                prompt=prompt,
                response_mime_type="backend.ication/json",
                response_schema=List[DocAnalysisResult]
            )
            return results, tokens
        except Exception as e:
            logger.error(f"Doc Intel failed: {e}")
            raise
