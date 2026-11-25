from typing import Dict, Any

class AnalyticsAggregator:
    @staticmethod
    def calculate_funnel_conversion(applied: int, screened: int, interview: int, hired: int) -> Dict[str, float]:
        if applied == 0:
            return {"screen_rate": 0.0, "interview_rate": 0.0, "hire_rate": 0.0}
        return {
            "screen_rate": round((screened / applied) * 100.0, 1),
            "interview_rate": round((interview / applied) * 100.0, 1),
            "hire_rate": round((hired / applied) * 100.0, 1)
        }
