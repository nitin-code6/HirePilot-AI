from typing import Dict, Any
from app.agents.specialized import SpecializedAgents

class SupervisorOrchestrator:
    """
    Supervisor Agent that accurately classifies HR prompt intent,
    routes to the specialized agent, and coordinates approval flags.
    """

    @staticmethod
    def route_intent(prompt: str) -> str:
        p = prompt.lower()
        # High specificity priority checks
        if any(w in p for w in ["draft email", "draft interview", "invitation", "send email", "email", "communication"]):
            return "communication_agent"
        elif any(w in p for w in ["prepare interview", "schedule interview", "interview slot", "interview for", "available slot"]):
            return "interview_agent"
        elif any(w in p for w in ["screen", "find the best candidate", "matching candidate", "best candidate", "qualification score"]):
            return "resume_screening_agent"
        elif any(w in p for w in ["shortlist", "candidate", "applicant", "talent pool", "profile"]):
            return "candidate_agent"
        elif any(w in p for w in ["funnel", "analytics", "statistic", "metric", "trend", "report"]):
            return "analytics_agent"
        elif any(w in p for w in ["create a job", "create job", "job opening", "requisition", "opening for", "new job", "backend developer", "frontend developer", "role"]):
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
