import unittest
from unittest.mock import MagicMock
from app.pipelines.fraud_pipeline import FraudPipeline, FraudAnalysisResult

class TestFraudPipeline(unittest.TestCase):
    def setUp(self):
        self.mock_llm = MagicMock()
        self.pipeline = FraudPipeline(self.mock_llm)

    def test_fraud_analysis_success(self):
        # Mock structured output
        mock_result = [
            FraudAnalysisResult(
                transaction_id="TX123",
                risk_level="High",
                anomaly_explanation="Large amount",
                reasoning="Suspicious activity",
                confidence_score=95
            )
        ]
        self.mock_llm.get_structured_output.return_value = (mock_result, 150)
        
        results, tokens = self.pipeline.analyze_transactions([{"amount": 10000}])
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].risk_level, "High")
        self.assertEqual(tokens, 150)

if __name__ == "__main__":
    unittest.main()
