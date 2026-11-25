import unittest
from app.mcp.tools import MCPToolsRegistry

class TestMCPToolsDirect(unittest.TestCase):
    def test_list_jobs(self):
        jobs = MCPToolsRegistry.list_jobs()
        self.assertIsInstance(jobs, list)

    def test_available_slots(self):
        slots = MCPToolsRegistry.get_available_slots()
        self.assertTrue(len(slots) > 0)
        self.assertIn("start", slots[0])

    def test_draft_email(self):
        draft = MCPToolsRegistry.draft_email("test@example.com", "Test User", "Backend Dev")
        self.assertEqual(draft["recipient_email"], "test@example.com")
        self.assertIn("Interview Invitation", draft["subject"])

if __name__ == "__main__":
    unittest.main()
