import unittest
from app.services.analytics_aggregator import AnalyticsAggregator

class TestAnalyticsAggregator(unittest.TestCase):
    def test_zero_applied(self):
        res = AnalyticsAggregator.calculate_funnel_conversion(0, 0, 0, 0)
        self.assertEqual(res["screen_rate"], 0.0)

    def test_conversion_calculation(self):
        res = AnalyticsAggregator.calculate_funnel_conversion(100, 75, 25, 5)
        self.assertEqual(res["screen_rate"], 75.0)
        self.assertEqual(res["interview_rate"], 25.0)
        self.assertEqual(res["hire_rate"], 5.0)

if __name__ == "__main__":
    unittest.main()
