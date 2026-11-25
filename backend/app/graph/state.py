from typing import TypedDict, List, Dict, Any, Optional
from langchain_core.messages import BaseMessage

class RecruitmentState(TypedDict):
    messages: List[BaseMessage]
    current_intent: Optional[str]
    target_agent: Optional[str]
    agent_output: Optional[str]
    requires_approval: bool
    approval_payload: Optional[Dict[str, Any]]
    action_result: Optional[Dict[str, Any]]
