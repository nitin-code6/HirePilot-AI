import unittest
from app.graph.guardrails import StateGuardrails

class TestStateGuardrails(unittest.TestCase):
    def test_unauthorized_action(self):
        self.assertFalse(StateGuardrails.validate_action("publish_job", "recruiter"))
        self.assertFalse(StateGuardrails.validate_action("delete_job", "recruiter"))

    def test_authorized_action(self):
        self.assertTrue(StateGuardrails.validate_action("publish_job", "admin"))
        self.assertTrue(StateGuardrails.validate_action("publish_job", "hr_manager"))

if __name__ == "__main__":
    unittest.main()
