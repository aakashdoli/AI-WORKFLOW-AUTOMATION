from pydantic import BaseModel, Field
from backend.services.llm_service import LLMService
from backend.utils.logger import logger
from typing import List

class KPIInsight(BaseModel):
    metric_name: str
    current_value: float
    trend: str # Improving, Declining, Stable
    insight: str

class ExecutiveReport(BaseModel):
    management_summary: str
    key_insights: List[KPIInsight]
    recommendations: List[str]
    strategic_priority: str # High, Medium, Low

class KPIPipeline:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def generate_report(self, operational_metrics: dict) -> tuple[ExecutiveReport, int]:
        logger.info("Generating executive KPI report")
        
        prompt = f"""
        Generate a management-level executive report based on the following operational metrics:
        
        Metrics:
        {operational_metrics}
        
        The report must include:
        1. A high-level management summary.
        2. A list of specific KPI insights (metric, value, trend, insight).
        3. 3-5 actionable recommendations.
        4. Overall strategic priority for the next quarter.
        """
        
        try:
            report, tokens = self.llm_service.get_structured_output(
                prompt=prompt,
                response_mime_type="backend.ication/json",
                response_schema=ExecutiveReport
            )
            logger.info("Executive report generated successfully")
            return report, tokens
        except Exception as e:
            logger.error(f"KPI reporting failed: {e}")
            raise
