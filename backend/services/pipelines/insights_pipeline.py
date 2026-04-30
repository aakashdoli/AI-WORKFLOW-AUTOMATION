from typing import List
from pydantic import BaseModel
from backend.services.llm_service import LLMService
from backend.utils.logger import logger

class OperationalInsight(BaseModel):
    category: str
    finding: str
    recommendation: str
    impact_level: str # High, Medium, Low

class InsightsPipeline:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def generate_system_insights(self, execution_history: List[dict]) -> List[OperationalInsight]:
        logger.info("Analyzing system execution history for operational insights")
        
        prompt = f"""
        Analyze the following AI workflow execution history. 
        Identify patterns, bottlenecks, or areas for improvement.
        
        History:
        {execution_history}
        
        Return a list of operational insights including:
        1. category (Cost, Performance, Accuracy)
        2. finding (what you observed)
        3. recommendation (what should be done)
        4. impact_level (High, Medium, Low)
        """
        
        try:
            results, tokens = self.llm_service.get_structured_output(
                prompt=prompt,
                response_mime_type="backend.ication/json",
                response_schema=List[OperationalInsight]
            )
            return results
        except Exception as e:
            logger.error(f"Failed to generate system insights: {e}")
            return []
