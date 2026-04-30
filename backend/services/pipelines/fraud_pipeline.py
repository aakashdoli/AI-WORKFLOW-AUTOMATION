from typing import List
from pydantic import BaseModel, Field
from backend.services.llm_service import LLMService
from backend.utils.logger import logger

class FraudAnalysisResult(BaseModel):
    transaction_id: str
    risk_level: str = Field(..., description="High, Medium, or Low")
    anomaly_explanation: str
    reasoning: str
    confidence_score: int = Field(..., ge=0, le=100)

class FraudPipeline:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def analyze_transactions(self, transactions: List[dict]) -> tuple[List[FraudAnalysisResult], int]:
        logger.info(f"Starting fraud analysis for {len(transactions)} transactions")
        
        prompt = f"""
        Analyze the following financial transactions for potential fraud or anomalies.
        Risk Levels: High (Immediate action), Medium (Review required), Low (Safe).
        
        Transactions:
        {transactions}
        
        For each transaction, provide:
        1. transaction_id
        2. risk_level
        3. anomaly_explanation (what looks suspicious)
        4. reasoning (detailed AI logic)
        5. confidence_score (0-100)
        """
        
        try:
            results, tokens = self.llm_service.get_structured_output(
                prompt=prompt,
                response_mime_type="backend.ication/json",
                response_schema=List[FraudAnalysisResult]
            )
            logger.info("Fraud analysis completed successfully")
            return results, tokens
        except Exception as e:
            logger.error(f"Fraud analysis failed: {e}")
            raise
