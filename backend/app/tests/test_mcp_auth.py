import unittest
from app.mcp.auth import MCPToolAuthorizer

class TestMCPAuth(unittest.TestCase):
    def test_admin_access(self):
        self.assertTrue(MCPToolAuthorizer.is_authorized("admin", "create_job"))
        self.assertTrue(MCPToolAuthorizer.is_authorized("admin", "screen_candidate"))

    def test_interviewer_restrictions(self):
        self.assertFalse(MCPToolAuthorizer.is_authorized("interviewer", "create_job"))

if __name__ == "__main__":
    unittest.main()
