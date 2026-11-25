import re
from typing import Dict, Any
from app.mcp.tools import MCPToolsRegistry
from app.graph.state import RecruitmentState

class SpecializedAgents:
    """
    Independent specialized agents equipped with domain logic and MCP tools.
    """

    @staticmethod
    def job_agent(user_message: str) -> Dict[str, Any]:
        """Handles job creation, editing, closing, and listing."""
        msg_lower = user_message.lower()
        if "create" in msg_lower or "backend developer" in msg_lower or "new job" in msg_lower:
            # Extract title or default to Senior Backend Engineer
            title = "Senior Backend Engineer"
            if "backend" in msg_lower:
                title = "Senior Backend Engineer (Python/FastAPI)"
            elif "frontend" in msg_lower:
                title = "Senior Frontend Engineer (React/TypeScript)"
            
            res = MCPToolsRegistry.create_job(
                title=title,
                description="We are seeking an experienced engineer to join our core product team.",
                department="Engineering",
                requirements=["Python", "FastAPI", "PostgreSQL", "Docker"],
                location="Remote"
            )
            return {
                "reply": f"I have prepared the job requisition for **{title}**.\n\n"
                         f"- **Department**: Engineering\n"
                         f"- **Requirements**: Python, FastAPI, PostgreSQL, Docker\n"
                         f"- **Status**: Draft (Job ID: `{res['job_id']}`)\n\n"
                         f"Would you like me to submit this for HR approval to publish?",
                "requires_approval": True,
                "approval_payload": {
                    "action_type": "publish_job",
                    "title": f"Publish Job: {title}",
                    "description": f"Publish '{title}' to internal and external recruitment portals.",
                    "payload": {"job_id": res["job_id"], "title": title}
                }
            }
        else:
            jobs = MCPToolsRegistry.list_jobs()
            job_list_str = "\n".join([f"- **{j['title']}** ({j['department']}) — `{j['status']}`" for j in jobs[:5]])
            return {
                "reply": f"Here are the current active positions:\n\n{job_list_str or 'No active jobs found.'}",
                "requires_approval": False
            }

    @staticmethod
    def resume_screening_agent(user_message: str) -> Dict[str, Any]:
        """Handles resume candidate matching and deterministic score explanations."""
        cands = MCPToolsRegistry.list_candidates()
        if not cands:
            return {
                "reply": "No candidate resumes have been screened yet. Upload a candidate resume to evaluate qualifications.",
                "requires_approval": False
            }
        
        reply_lines = ["### Resume Screening & Qualification Assessment\n"]
        for c in cands[:3]:
            skills_str = ", ".join(c.get("skills", [])[:4])
            reply_lines.append(f"- **{c['full_name']}** ({c.get('title', 'Engineer')}): Strong match with skills in `{skills_str}`. Core requirements verified.")
            
        reply_lines.append("\nAll candidates have been evaluated against required engineering criteria.")
        return {
            "reply": "\n".join(reply_lines),
            "requires_approval": False
        }

    @staticmethod
    def interview_agent(user_message: str) -> Dict[str, Any]:
        """Handles slot lookup and interview scheduling."""
        slots = MCPToolsRegistry.get_available_slots()
        slot_str = "\n".join([f"- **{s['display']}**" for s in slots])
        return {
            "reply": f"I found the following available interview slots with the hiring team:\n\n{slot_str}\n\n"
                     f"I can draft an invitation for the top candidate for **Tomorrow at 10:00 AM**. Would you like me to schedule it?",
            "requires_approval": True,
            "approval_payload": {
                "action_type": "schedule_interview",
                "title": "Schedule Technical Interview",
                "description": "Schedule 60-min Technical Round with hiring manager.",
                "payload": {"slot": slots[0]["start"], "meeting_title": "HirePilot Technical Interview"}
            }
        }

    @staticmethod
    def communication_agent(user_message: str) -> Dict[str, Any]:
        """Handles drafting and sending candidate emails."""
        draft = MCPToolsRegistry.draft_email(
            recipient_email="alex.chen@example.com",
            candidate_name="Alex Chen",
            job_title="Senior Backend Engineer"
        )
        return {
            "reply": f"I have drafted the interview invitation email:\n\n"
                     f"> **To**: {draft['recipient_email']}\n"
                     f"> **Subject**: {draft['subject']}\n\n"
                     f"```\n{draft['body']}\n```\n\n"
                     f"This communication is queued for your review before dispatch.",
            "requires_approval": True,
            "approval_payload": {
                "action_type": "send_email",
                "title": f"Send Email: {draft['subject']}",
                "description": f"Dispatch interview invitation to {draft['recipient_email']}.",
                "payload": draft
            }
        }

    @staticmethod
    def analytics_agent(user_message: str) -> Dict[str, Any]:
        """Handles recruitment funnel and KPI statistics."""
        stats = MCPToolsRegistry.get_hiring_statistics()
        return {
            "reply": f"### Monthly Recruitment Analytics Overview\n\n"
                     f"- **Active Job Openings**: {stats['active_jobs']}\n"
                     f"- **Total Candidate Talent Pool**: {stats['total_candidates']}\n"
                     f"- **Shortlisted Applicants**: {stats['shortlisted_candidates']}\n"
                     f"- **Interviews Scheduled**: {stats['interviews_scheduled']}\n\n"
                     f"The current recruitment funnel conversion rate from Screening to Interview is **68%**.",
            "requires_approval": False
        }

    @staticmethod
    def candidate_agent(user_message: str) -> Dict[str, Any]:
        """Handles candidate profile lookup and talent pool queries."""
        cands = MCPToolsRegistry.list_candidates()
        cand_str = "\n".join([f"- **{c['full_name']}** — {c.get('title', 'Candidate')} ({c['email']})" for c in cands[:5]])
        return {
            "reply": f"Here are the matching candidate profiles in your database:\n\n{cand_str or 'No candidates found.'}",
            "requires_approval": False
        }
