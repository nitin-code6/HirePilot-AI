from typing import Dict, Any

class HumanApprovalRouter:
    """
    Decides whether an action payload requires HR executive approval before execution.
    """
    @staticmethod
    def requires_approval(action_type: str, payload: Dict[str, Any]) -> bool:
        crit_actions = ["publish_job", "send_email", "schedule_interview", "cancel_interview"]
        return action_type in crit_actions
