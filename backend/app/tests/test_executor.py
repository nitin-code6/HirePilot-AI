import unittest
from app.services.action_executor import ActionExecutor

class TestActionExecutor(unittest.TestCase):
    def test_execution_payload_logging(self):
        res = ActionExecutor.execute("publish_job", {"job_id": "job_123"})
        self.assertEqual(res["status"], "completed")
        self.assertEqual(res["action"], "publish_job")
        self.assertEqual(res["details"]["job_id"], "job_123")

if __name__ == "__main__":
    unittest.main()
