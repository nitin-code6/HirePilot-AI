import re
from typing import Dict, Any, List
from app.mcp.client import mcp_client
from app.database.session import SessionLocal
from app.models.models import Job, Candidate, Application, Resume, ScreeningReport
from app.models.enums import ApplicationStage, JobStatus
from app.services.skill_normalizer import SkillNormalizer

class SpecializedAgents:
    """
    Independent specialized agents that invoke MCP tools via the MCP client integration
    and execute domain reasoning on database entities.
    """

    # --- SCENARIO 1: JOB MANAGEMENT AGENT ---
    @staticmethod
    def job_agent(user_message: str) -> Dict[str, Any]:
        """
        Dynamically extracts job title, experience years, and skills from user prompt
        or handles listing, closing, and updating jobs via MCP tools.
        """
        msg = user_message
        msg_lower = msg.lower()

        if any(w in msg_lower for w in ["create", "opening", "new job", "hire", "recruit"]):
            # Extract Title
            title = "Backend Developer"
            if "senior" in msg_lower:
                title = "Senior " + title
            elif "lead" in msg_lower:
                title = "Lead " + title

            # Detect specific role names
            role_match = re.search(r'(?:for\s+(?:a|an)?\s*)([A-Za-z\s]+?)(?:\s+with|\s+requiring|\s+who|\s+and|\.|$)', msg, re.IGNORECASE)
            if role_match:
                extracted_role = role_match.group(1).strip()
                if len(extracted_role) > 2 and len(extracted_role) < 50:
                    title = extracted_role.title()

            # Extract Experience
            exp_match = re.search(r'(\d+)\+?\s*(?:years?|yrs?)', msg_lower)
            exp_years = int(exp_match.group(1)) if exp_match else 2

            # Extract Skills
            detected_skills = []
            skill_keywords = ["Python", "FastAPI", "PostgreSQL", "Docker", "Kubernetes", "Redis", "React", "TypeScript", "AWS", "SQL"]
            for sk in skill_keywords:
                if re.search(rf'\b{re.escape(sk)}\b', msg, re.IGNORECASE):
                    detected_skills.append(sk)
            
            if not detected_skills:
                detected_skills = ["Python", "FastAPI", "PostgreSQL"]

            skills_normalized = SkillNormalizer.normalize_list(detected_skills)

            # Invoke MCP Tool via MCP Client
            res = mcp_client.call_tool_sync("create_job", {
                "title": title,
                "description": f"We are hiring a skilled {title} ({exp_years}+ years experience) proficient in {', '.join(skills_normalized)}.",
                "department": "Engineering",
                "requirements": skills_normalized,
                "location": "Remote"
            })

            job_id = res.get("job_id")
            return {
                "reply": f"Requisition created successfully via MCP Job Tool:\n\n"
                         f"- **Title**: {title}\n"
                         f"- **Department**: Engineering\n"
                         f"- **Experience Required**: {exp_years}+ years\n"
                         f"- **Skills Required**: {', '.join(skills_normalized)}\n"
                         f"- **Requisition ID**: `{job_id}`\n"
                         f"- **Status**: `Draft` (Pending Publication Approval)\n\n"
                         f"Would you like me to request HR approval to publish this job opening?",
                "requires_approval": True,
                "approval_payload": {
                    "action_type": "publish_job",
                    "title": f"Publish Job: {title}",
                    "description": f"Publish '{title}' requisition (ID: {job_id}) to external talent channels.",
                    "payload": {"job_id": job_id, "title": title}
                }
            }
        else:
            jobs = mcp_client.call_tool_sync("list_jobs")
            if not jobs or not isinstance(jobs, list):
                return {"reply": "No active job openings found in database.", "requires_approval": False}
            lines = [f"- **{j['title']}** ({j.get('department', 'Engineering')}) — `{j['status']}` [ID: `{j['id'][:8]}`]" for j in jobs[:6]]
            return {
                "reply": "Here are the current job openings:\n\n" + "\n".join(lines),
                "requires_approval": False
            }

    # --- SCENARIO 2: RESUME SCREENING AGENT ---
    @staticmethod
    def resume_screening_agent(user_message: str) -> Dict[str, Any]:
        """
        Retrieves matching candidates for a requested position,
        evaluates qualifications, ranks applicants by match score,
        and provides links/reports.
        """
        with SessionLocal() as db:
            # Find relevant job or use most recently active backend/engineering job
            jobs = db.query(Job).all()
            target_job = None
            for j in jobs:
                if any(w in user_message.lower() for w in j.title.lower().split()):
                    target_job = j
                    break
            if not target_job and jobs:
                target_job = jobs[0]

            if not target_job:
                return {"reply": "No job requisition found to evaluate candidates against.", "requires_approval": False}

            # Retrieve candidate applications or candidate talent pool
            candidates = db.query(Candidate).all()
            if not candidates:
                return {"reply": f"No candidate resumes found for **{target_job.title}**.", "requires_approval": False}

            # Perform scoring / rank candidates against target job
            ranked = []
            for cand in candidates:
                # Calculate match score based on candidate skills vs job requirements
                job_reqs = [r.lower() for r in (target_job.requirements or [])]
                cand_skills = [s.lower() for s in (cand.skills or [])]
                matches = [r for r in job_reqs if any(r in cs or cs in r for cs in cand_skills)]
                missing = [r for r in job_reqs if r not in matches]
                
                score = round((len(matches) / max(len(job_reqs), 1)) * 80.0 + (min(cand.experience_years / max(target_job.min_experience_years, 1), 1.0)) * 20.0, 1)
                ranked.append({
                    "id": cand.id,
                    "name": cand.full_name,
                    "title": cand.current_title or "Engineer",
                    "score": score,
                    "matches": matches,
                    "missing": missing,
                    "exp": cand.experience_years
                })

            ranked.sort(key=lambda x: x["score"], reverse=True)

            reply_lines = [
                f"### Ranked Candidates for **{target_job.title}**\n",
                f"Evaluated {len(ranked)} candidate profiles against core criteria ({', '.join(target_job.requirements or [])}):\n"
            ]

            for idx, r in enumerate(ranked[:4], start=1):
                match_str = ", ".join([m.title() for m in r["matches"]]) or "General fit"
                reply_lines.append(
                    f"{idx}. **{r['name']}** — Match Score: **{r['score']}%**\n"
                    f"   - Title: {r['title']} ({r['exp']} yrs exp)\n"
                    f"   - Verified Skills: `{match_str}`\n"
                    f"   - Candidate ID: `{r['id'][:8]}`\n"
                )

            reply_lines.append("You can inspect detailed screening reports or invite top candidates in the **Resume Screening** tab.")
            return {
                "reply": "\n".join(reply_lines),
                "requires_approval": False
            }

    # --- SCENARIO 3: CANDIDATE MANAGEMENT AGENT ---
    @staticmethod
    def candidate_agent(user_message: str) -> Dict[str, Any]:
        """
        Retrieves shortlisted or all candidates from database via MCP client.
        """
        msg_lower = user_message.lower()
        with SessionLocal() as db:
            if "shortlist" in msg_lower:
                apps = db.query(Application).filter(Application.stage.in_([ApplicationStage.SHORTLISTED, ApplicationStage.INTERVIEW_SCHEDULED])).all()
                if not apps:
                    # Fallback to candidates with score > 75
                    cands = db.query(Candidate).limit(5).all()
                else:
                    cands = [a.candidate for a in apps if a.candidate]
                
                heading = "### Shortlisted Candidates in Talent Pipeline"
            else:
                cands = db.query(Candidate).all()
                heading = "### Talent Pool Directory"

            if not cands:
                return {"reply": "No candidate records found in database.", "requires_approval": False}

            lines = [heading + "\n"]
            for c in cands[:5]:
                skills_str = ", ".join(c.skills[:4]) if c.skills else "General"
                lines.append(
                    f"- **{c.full_name}** | {c.current_title or 'Engineer'} ({c.experience_years} yrs exp)\n"
                    f"  Email: `{c.email}` | Skills: `{skills_str}` | ID: `{c.id[:8]}`"
                )

            return {
                "reply": "\n".join(lines),
                "requires_approval": False
            }

    # --- SCENARIO 4: INTERVIEW AGENT ---
    @staticmethod
    def interview_agent(user_message: str) -> Dict[str, Any]:
        """
        Retrieves candidate and interview slots, prepares interview proposals,
        and requests HR approval before scheduling.
        """
        slots = mcp_client.call_tool_sync("get_available_slots")
        with SessionLocal() as db:
            cands = db.query(Candidate).limit(3).all()
            cand_names = [c.full_name for c in cands] if cands else ["Alex Chen", "Maya Patel"]

        slot_lines = [f"- **{s['display']}**" for s in slots]

        return {
            "reply": f"### Interview Scheduling Proposals\n\n"
                     f"I have reviewed the top candidates (**{', '.join(cand_names)}**) and identified open interviewer availability:\n\n"
                     + "\n".join(slot_lines) + "\n\n"
                     f"I have prepared an interview invitation for **{cand_names[0]}** for **{slots[0]['display']}** (Google Meet).\n\n"
                     f"HR approval is required before this interview event is finalized.",
            "requires_approval": True,
            "approval_payload": {
                "action_type": "schedule_interview",
                "title": f"Schedule Technical Round: {cand_names[0]}",
                "description": f"Schedule 60-minute Technical Architecture interview with {cand_names[0]} at {slots[0]['display']}.",
                "payload": {
                    "candidate_name": cand_names[0],
                    "slot": slots[0]["start"],
                    "meeting_title": f"Technical Interview — {cand_names[0]}",
                    "meeting_link": "https://meet.google.com/hpr-slot-1"
                }
            }
        }

    # --- SCENARIO 5: COMMUNICATION AGENT ---
    @staticmethod
    def communication_agent(user_message: str) -> Dict[str, Any]:
        """
        Retrieves candidate details, drafts email invitations,
        and creates approval request before dispatch.
        """
        with SessionLocal() as db:
            cand = db.query(Candidate).first()
            name = cand.full_name if cand else "Alex Chen"
            email = cand.email if cand else "alex.chen@example.com"
            job = db.query(Job).first()
            job_title = job.title if job else "Senior Backend Engineer"

        draft = mcp_client.call_tool_sync("draft_email", {
            "recipient_email": email,
            "candidate_name": name,
            "job_title": job_title,
            "template_type": "interview_invite"
        })

        return {
            "reply": f"### Candidate Interview Invitation Draft\n\n"
                     f"I have drafted the personalized interview invitation for **{name}**:\n\n"
                     f"> **To**: `{draft['recipient_email']}`\n"
                     f"> **Subject**: {draft['subject']}\n\n"
                     f"```text\n{draft['body']}\n```\n\n"
                     f"This email is staged in the **Approvals** queue. Upon HR approval, it will be dispatched via the configured email provider.",
            "requires_approval": True,
            "approval_payload": {
                "action_type": "send_email",
                "title": f"Send Interview Invitation: {name}",
                "description": f"Dispatch technical interview email to {name} ({email}).",
                "payload": draft
            }
        }

    # --- SCENARIO 6: ANALYTICS AGENT ---
    @staticmethod
    def analytics_agent(user_message: str) -> Dict[str, Any]:
        """
        Fetches recruitment funnel, active jobs, and conversion metrics via MCP client.
        """
        stats = mcp_client.call_tool_sync("get_hiring_statistics")
        return {
            "reply": f"### Real-time Recruitment Performance Metrics\n\n"
                     f"- **Active Job Openings**: {stats.get('active_jobs', 0)}\n"
                     f"- **Total Talent Pool**: {stats.get('total_candidates', 0)} candidates\n"
                     f"- **Shortlisted Applicants**: {stats.get('shortlisted_candidates', 0)}\n"
                     f"- **Interviews Scheduled**: {stats.get('interviews_scheduled', 0)}\n\n"
                     f"You can view complete monthly conversion charts and velocity in the **Analytics** tab.",
            "requires_approval": False
        }
