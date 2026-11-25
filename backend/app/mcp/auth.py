import logging
from typing import Dict, Any

logger = logging.getLogger("hirepilot.mcp.auth")

class MCPToolAuthorizer:
    @staticmethod
    def is_authorized(user_role: str, tool_name: str) -> bool:
        recruiter_tools = [
            "create_job", "list_jobs", "get_job_details",
            "list_candidates", "get_candidate_details",
            "screen_candidate", "get_screening_report",
            "get_available_slots", "draft_email", "get_hiring_statistics"
        ]
        if user_role in ["admin", "hr_manager"]:
            return True
        if user_role == "recruiter" and tool_name in recruiter_tools:
            return True
        return False
