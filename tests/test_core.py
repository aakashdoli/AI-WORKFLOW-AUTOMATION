import os
import sys
import unittest
from unittest.mock import MagicMock

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.database_service import DatabaseService, init_db
from app.pipelines.classification_pipeline import ClassificationPipeline, ClassificationResult

class TestAutomationPlatform(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DATABASE_URL"] = "sqlite:///:memory:"
        init_db()

    def setUp(self):
        self.db_service = DatabaseService()
        self.mock_llm = MagicMock()

    def test_database_init(self):
        workflow = self.db_service.create_workflow("Test Workflow")
        self.assertIsNotNone(workflow.id)
        self.assertEqual(workflow.name, "Test Workflow")

    def test_classification_logic(self):
        pipeline = ClassificationPipeline(self.mock_llm)
        self.mock_llm.get_structured_output.return_value = [
            ClassificationResult(ticket_id="101", category="Billing", priority="High", reasoning="Mocked")
        ]
        
        results = pipeline.classify_records([{"Ticket ID": "101", "Description": "Pay fail"}])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].category, "Billing")

    def tearDown(self):
        self.db_service.close()

if __name__ == "__main__":
    unittest.main()
