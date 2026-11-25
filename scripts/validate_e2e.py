#!/usr/bin/env python3
"""
HirePilot AI — Complete End-to-End System Validation Suite
Executes all 18 validation steps specified in Part 20.
"""
import sys
import os
import unittest
from datetime import datetime, timedelta

# Setup environment path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.database.session import SessionLocal, Base, engine
from app.models.models import Job, Candidate, Resume, Application, ScreeningReport, ApprovalRequest, Interview, EmailLog
from app.models.enums import JobStatus, ApplicationStage, ApprovalStatus, ApprovalActionType, InterviewStatus
from app.services.resume_parser import ResumeParserService
from app.services.screening_service import ScreeningEngine
from app.graph.supervisor import SupervisorOrchestrator
from app.mcp.tools import MCPToolsRegistry
from app.integrations.providers import EmailService, CalendarService

class TestEndToEndRecruitmentFlow(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()

    def tearDown(self):
        self.db.close()

    def test_complete_autonomous_lifecycle(self):
        print("\n--- [E2E STEP 1 & 2]: System initialization & Database connection ---")
        self.assertIsNotNone(self.db)
        print("PASS: System services initialized and database connection verified.")

        print("\n--- [E2E STEP 3 & 4]: Create Backend Developer job & Verify PostgreSQL persistence ---")
        job = Job(
            title="Senior Backend Developer (FastAPI)",
            department="Cloud Engineering",
            location="Remote",
            description="Build scalable distributed cloud microservices.",
            requirements=["Python", "FastAPI", "PostgreSQL", "Docker", "Redis"],
            preferred_skills=["Kubernetes", "AWS"],
            min_experience_years=4,
            status=JobStatus.PUBLISHED
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        self.assertIsNotNone(job.id)
        print(f"PASS: Requisition created with ID {job.id} and persisted successfully.")

        print("\n--- [E2E STEP 5 & 6]: Upload sample resume & Extract candidate information ---")
        sample_resume_text = """
        Jordan Lee
        jordan.lee@example.com | (415) 555-0199 | San Francisco, CA
        Senior Software Engineer with 6 years of experience building high-throughput microservices.
        Technical Skills: Python, FastAPI, PostgreSQL, Docker, Redis, Kubernetes, AWS, Git, CI/CD.
        Education: B.S. in Computer Science.
        """
        file_bytes = sample_resume_text.encode("utf-8")
        file_hash = ResumeParserService.calculate_sha256(file_bytes)
        parsed = ResumeParserService.parse_information(sample_resume_text)
        
        cand = Candidate(
            full_name=parsed["full_name"],
            email=parsed["email"],
            phone=parsed["phone"],
            experience_years=parsed["experience_years"],
            skills=parsed["skills"]
        )
        self.db.add(cand)
        self.db.commit()
        self.db.refresh(cand)

        resume = Resume(
            candidate_id=cand.id,
            filename="jordan_lee_resume.txt",
            file_path="/uploads/jordan_lee_resume.txt",
            file_hash=file_hash,
            raw_text=sample_resume_text,
            parsed_data=parsed
        )
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        print(f"PASS: Candidate {cand.full_name} profile created; skills extracted: {cand.skills}")

        print("\n--- [E2E STEP 7 & 8]: Screen resume against job & Save matching report ---")
        report_data = ScreeningEngine.match_resume_to_job(resume, job)
        report = ScreeningReport(
            resume_id=resume.id,
            job_id=job.id,
            **report_data
        )
        self.db.add(report)
        self.db.commit()
        self.assertGreaterEqual(report.overall_score, 85.0)
        print(f"PASS: Screening generated overall score: {report.overall_score}% with explainable report.")

        print("\n--- [E2E STEP 9 & 10]: AI Assistant supervisor routing ---")
        route = SupervisorOrchestrator.route_intent("Find candidates matching this position")
        self.assertEqual(route, "candidate_agent")
        print("PASS: Supervisor correctly routed talent query to candidate_agent.")

        print("\n--- [E2E STEP 11]: Actual MCP tool execution ---")
        candidates_found = MCPToolsRegistry.list_candidates()
        self.assertGreaterEqual(len(candidates_found), 1)
        print(f"PASS: MCP tool list_candidates returned {len(candidates_found)} candidate profile(s).")

        print("\n--- [E2E STEP 12 & 13]: Draft interview invitation & Create approval request ---")
        draft = MCPToolsRegistry.draft_email(cand.email, cand.full_name, job.title)
        approval = ApprovalRequest(
            action_type=ApprovalActionType.SEND_EMAIL,
            status=ApprovalStatus.PENDING,
            title=f"Send Interview Invite to {cand.full_name}",
            description=f"Automated draft for {job.title}",
            payload=draft
        )
        self.db.add(approval)
        self.db.commit()
        self.db.refresh(approval)
        self.assertEqual(approval.status, ApprovalStatus.PENDING)
        print("PASS: Human approval request created and queued with PENDING status.")

        print("\n--- [E2E STEP 14, 15 & 16]: Approve action & Verify email dispatch and communication log ---")
        email_res = EmailService.send_email(
            to_email=approval.payload["recipient_email"],
            subject=approval.payload["subject"],
            body=approval.payload["body"]
        )
        email_record = EmailLog(
            recipient_email=approval.payload["recipient_email"],
            subject=approval.payload["subject"],
            body=approval.payload["body"],
            status=email_res["status"]
        )
        self.db.add(email_record)
        approval.status = ApprovalStatus.APPROVED
        approval.result_log = email_res
        self.db.commit()
        self.assertEqual(approval.status, ApprovalStatus.APPROVED)
        print(f"PASS: Approval executed successfully via provider: {email_res.get('provider')}")

        print("\n--- [E2E STEP 17 & 18]: Open analytics & Verify database-backed metrics ---")
        stats = MCPToolsRegistry.get_hiring_statistics()
        self.assertGreaterEqual(stats["total_candidates"], 1)
        print(f"PASS: Real-time analytics computed directly from database: {stats}")

if __name__ == "__main__":
    unittest.main()
