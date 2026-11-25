from typing import Dict, Any
from app.graph.state import RecruitmentState
from app.agents.specialized import SpecializedAgents

class SupervisorOrchestrator:
    """
    Supervisor Agent that classifies user intent, routes to specialized agents,
    and constructs structured multi-agent state.
    """

    @staticmethod
    def route_intent(prompt: str) -> str:
        p = prompt.lower()
        if any(w in p for w in ["email", "invite", "draft", "message", "communication"]):
            return "communication_agent"
        elif any(w in p for w in ["candidate", "applicant", "profile", "pool", "find candidate"]):
            return "candidate_agent"
        elif any(w in p for w in ["screen", "resume", "score", "match", "qualif"]):
            return "resume_screening_agent"
        elif any(w in p for w in ["interview", "slot", "calendar", "schedule"]):
            return "interview_agent"
        elif any(w in p for w in ["analytic", "funnel", "metric", "report", "stat", "rate"]):
            return "analytics_agent"
        elif any(w in p for w in ["job", "role", "position", "create job", "jd", "description"]):
            return "job_agent"
        return "job_agent"

    @classmethod
    def execute(cls, user_message: str) -> Dict[str, Any]:
        agent_key = cls.route_intent(user_message)
        
        agent_dispatch = {
            "job_agent": (SpecializedAgents.job_agent, "Job Management Agent"),
            "resume_screening_agent": (SpecializedAgents.resume_screening_agent, "Resume Screening Agent"),
            "interview_agent": (SpecializedAgents.interview_agent, "Interview Scheduling Agent"),
            "communication_agent": (SpecializedAgents.communication_agent, "Candidate Communication Agent"),
            "analytics_agent": (SpecializedAgents.analytics_agent, "Recruitment Analytics Agent"),
            "candidate_agent": (SpecializedAgents.candidate_agent, "Candidate Management Agent")
        }

        func, agent_name = agent_dispatch.get(agent_key, (SpecializedAgents.job_agent, "Job Management Agent"))
        result = func(user_message)
        
        return {
            "agent_used": agent_name,
            "reply": result["reply"],
            "requires_approval": result.get("requires_approval", False),
            "approval_payload": result.get("approval_payload")
        }
