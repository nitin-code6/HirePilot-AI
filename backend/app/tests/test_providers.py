import unittest
from app.integrations.providers import EmailService, CalendarService

class TestProvidersMock(unittest.TestCase):
    def test_mock_email_dispatch(self):
        res = EmailService.send_email("cand@example.com", "Test Subject", "Body")
        self.assertIn("cand@example.com", res.get("recipient", ""))
        self.assertEqual(res.get("provider"), "mock")

    def test_mock_calendar_dispatch(self):
        res = CalendarService.create_meeting("Interview", "2026-11-27T10:00:00", "2026-11-27T11:00:00", "cand@example.com")
        self.assertEqual(res.get("status"), "confirmed")
        self.assertTrue(res.get("meeting_url", "").startswith("https://meet.google.com/"))

if __name__ == "__main__":
    unittest.main()
