from typing import List
from backend.services.llm_service import LLMService

class SummarizationPipeline:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def generate_executive_summary(self, data_context: str) -> str:
        prompt = f"""
        Generate an executive operational summary for the following data:
        
        Data Context:
        {data_context}
        
        The summary should include:
        1. Key trends or recurring issues.
        2. High-priority items that need immediate attention.
        3. Recommendations for operational improvements.
        4. A brief conclusion.
        
        Format the output in professional business markdown.
        """
        
        summary = self.llm_service.generate_content(prompt)
        return summary
