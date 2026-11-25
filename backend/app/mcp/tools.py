from typing import Dict, Any, List
from app.database.session import SessionLocal
from app.models.models import Job, Candidate, Application, Resume, Interview, ScreeningReport, EmailLog
from app.models.enums import JobStatus, ApplicationStage, InterviewStatus
from app.services.screening_service import ScreeningEngine

class MCPToolsRegistry:
    """
    Standard Model Context Protocol (MCP) recruitment tool implementations.
    These tools execute directly against the persistent recruitment database.
    """

    # --- JOB TOOLS ---
    @staticmethod
    def create_job(title: str, description: str, department: str = "Engineering", requirements: List[str] = None, location: str = "Remote") -> Dict[str, Any]:
        with SessionLocal() as db:
            job = Job(
                title=title,
                description=description,
                department=department,
                requirements=requirements or [],
                location=location,
                status=JobStatus.DRAFT
            )
            db.add(job)
            db.commit()
            db.refresh(job)
            return {"status": "success", "job_id": job.id, "title": job.title, "job_status": job.status.value}

    @staticmethod
    def list_jobs(status: str = None) -> List[Dict[str, Any]]:
        with SessionLocal() as db:
            query = db.query(Job)
            if status:
                query = query.filter(Job.status == status)
            jobs = query.all()
            return [{"id": j.id, "title": j.title, "department": j.department, "status": j.status.value, "location": j.location} for j in jobs]

    @staticmethod
    def get_job_details(job_id: str) -> Dict[str, Any]:
        with SessionLocal() as db:
            job = db.query(Job).filter(Job.id == job_id).first()
            if not job:
                return {"error": f"Job {job_id} not found"}
            return {
                "id": job.id,
                "title": job.title,
                "department": job.department,
                "description": job.description,
                "requirements": job.requirements,
                "preferred_skills": job.preferred_skills,
                "status": job.status.value,
                "salary_range": job.salary_range
            }

    @staticmethod
    def update_job(job_id: str, title: str = None, description: str = None, status: str = None) -> Dict[str, Any]:
        with SessionLocal() as db:
            job = db.query(Job).filter(Job.id == job_id).first()
            if not job:
                return {"error": f"Job {job_id} not found"}
            if title:
                job.title = title
            if description:
                job.description = description
            if status:
                job.status = JobStatus(status)
            db.commit()
            return {"status": "success", "job_id": job.id, "updated_status": job.status.value}

    @staticmethod
    def close_job(job_id: str) -> Dict[str, Any]:
        with SessionLocal() as db:
            job = db.query(Job).filter(Job.id == job_id).first()
            if not job:
                return {"error": f"Job {job_id} not found"}
            job.status = JobStatus.CLOSED
            db.commit()
            return {"status": "success", "job_id": job.id, "status": "closed"}

    # --- CANDIDATE TOOLS ---
    @staticmethod
    def create_candidate(full_name: str, email: str, current_title: str = None, skills: List[str] = None, experience_years: float = 0.0) -> Dict[str, Any]:
        with SessionLocal() as db:
            cand = db.query(Candidate).filter(Candidate.email == email.lower()).first()
            if cand:
                return {"status": "existing", "candidate_id": cand.id, "full_name": cand.full_name}
            cand = Candidate(
                full_name=full_name,
                email=email.lower(),
                current_title=current_title,
                skills=skills or [],
                experience_years=experience_years
            )
            db.add(cand)
            db.commit()
            db.refresh(cand)
            return {"status": "created", "candidate_id": cand.id, "full_name": cand.full_name}

    @staticmethod
    def list_candidates(search: str = None) -> List[Dict[str, Any]]:
        with SessionLocal() as db:
            query = db.query(Candidate)
            if search:
                query = query.filter(Candidate.full_name.ilike(f"%{search}%") | Candidate.skills.cast(str).ilike(f"%{search}%"))
            candidates = query.all()
            return [{"id": c.id, "full_name": c.full_name, "email": c.email, "title": c.current_title, "skills": c.skills} for c in candidates]

    @staticmethod
    def get_candidate_details(candidate_id: str) -> Dict[str, Any]:
        with SessionLocal() as db:
            cand = db.query(Candidate).filter(Candidate.id == candidate_id).first()
            if not cand:
                return {"error": f"Candidate {candidate_id} not found"}
            return {
                "id": cand.id,
                "full_name": cand.full_name,
                "email": cand.email,
                "current_title": cand.current_title,
                "experience_years": cand.experience_years,
                "skills": cand.skills,
                "phone": cand.phone
            }

    @staticmethod
    def update_application_status(application_id: str, stage: str) -> Dict[str, Any]:
        with SessionLocal() as db:
            app = db.query(Application).filter(Application.id == application_id).first()
            if not app:
                return {"error": f"Application {application_id} not found"}
            app.stage = ApplicationStage(stage)
            db.commit()
            return {"status": "success", "application_id": app.id, "new_stage": app.stage.value}

    # --- RESUME SCREENING TOOLS ---
    @staticmethod
    def screen_candidate(resume_id: str, job_id: str) -> Dict[str, Any]:
        with SessionLocal() as db:
            resume = db.query(Resume).filter(Resume.id == resume_id).first()
            job = db.query(Job).filter(Job.id == job_id).first()
            if not resume or not job:
                return {"error": "Resume or Job not found"}
            report_data = ScreeningEngine.match_resume_to_job(resume, job)
            report = ScreeningReport(resume_id=resume.id, job_id=job.id, **report_data)
            db.add(report)
            db.commit()
            return {"status": "success", "report_id": report.id, "overall_score": report.overall_score, "explanation": report.explanation}

    @staticmethod
    def get_screening_report(resume_id: str) -> Dict[str, Any]:
        with SessionLocal() as db:
            report = db.query(ScreeningReport).filter(ScreeningReport.resume_id == resume_id).first()
            if not report:
                return {"error": "Report not found"}
            return {
                "overall_score": report.overall_score,
                "skills_score": report.skills_score,
                "matching_skills": report.matching_skills,
                "missing_skills": report.missing_skills,
                "strengths": report.strengths,
                "explanation": report.explanation
            }

    # --- INTERVIEW TOOLS ---
    @staticmethod
    def get_available_slots(interviewer_id: str = None) -> List[Dict[str, str]]:
        return [
            {"start": "2026-11-27T10:00:00", "end": "2026-11-27T11:00:00", "display": "Tomorrow 10:00 AM - 11:00 AM"},
            {"start": "2026-11-27T14:00:00", "end": "2026-11-27T15:00:00", "display": "Tomorrow 2:00 PM - 3:00 PM"},
            {"start": "2026-11-28T11:00:00", "end": "2026-11-28T12:00:00", "display": "Friday 11:00 AM - 12:00 PM"}
        ]

    @staticmethod
    def schedule_interview(application_id: str, title: str, scheduled_start: str, scheduled_end: str) -> Dict[str, Any]:
        with SessionLocal() as db:
            from datetime import datetime
            start_dt = datetime.fromisoformat(scheduled_start)
            end_dt = datetime.fromisoformat(scheduled_end)
            interview = Interview(
                application_id=application_id,
                title=title,
                scheduled_start=start_dt,
                scheduled_end=end_dt,
                meeting_link="https://meet.google.com/hpr-demo-slot",
                status=InterviewStatus.SCHEDULED
            )
            db.add(interview)
            db.commit()
            db.refresh(interview)
            return {"status": "scheduled", "interview_id": interview.id, "meeting_link": interview.meeting_link}

    # --- COMMUNICATION TOOLS ---
    @staticmethod
    def draft_email(recipient_email: str, candidate_name: str, job_title: str, template_type: str = "interview_invite") -> Dict[str, str]:
        if template_type == "interview_invite":
            subject = f"Interview Invitation: {job_title} at HirePilot"
            body = (
                f"Dear {candidate_name},\n\n"
                f"Thank you for applying for the {job_title} role at HirePilot. "
                f"We were impressed by your background and would love to invite you for an interview.\n\n"
                f"Please let us know your availability over the coming days.\n\n"
                f"Best regards,\nHirePilot Talent Acquisition Team"
            )
        else:
            subject = f"Update regarding your application for {job_title}"
            body = f"Dear {candidate_name},\n\nThank you for your interest in the {job_title} position."

        return {"recipient_email": recipient_email, "subject": subject, "body": body}

    # --- ANALYTICS TOOLS ---
    @staticmethod
    def get_hiring_statistics() -> Dict[str, Any]:
        with SessionLocal() as db:
            active_jobs = db.query(Job).filter(Job.status == JobStatus.PUBLISHED).count()
            total_cands = db.query(Candidate).count()
            shortlisted = db.query(Application).filter(Application.stage == ApplicationStage.SHORTLISTED).count()
            interviews = db.query(Interview).filter(Interview.status == InterviewStatus.SCHEDULED).count()
            return {
                "active_jobs": active_jobs,
                "total_candidates": total_cands,
                "shortlisted_candidates": shortlisted,
                "interviews_scheduled": interviews
            }
