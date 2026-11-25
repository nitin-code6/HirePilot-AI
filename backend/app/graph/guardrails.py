from typing import Dict, Any

class StateGuardrails:
    """
    Enforces that recruitment states maintain strict schema boundaries
    and never permit unauthorized execution of administrative actions.
    """
    @staticmethod
    def validate_action(action_type: str, user_role: str) -> bool:
        privileged_actions = ["publish_job", "send_email", "delete_job"]
        if action_type in privileged_actions and user_role not in ["admin", "hr_manager"]:
            return False
        return True
