from datetime import datetime, timedelta
from app.database.session import SessionLocal, Base, engine
from app.models.models import Company, User, Job, Candidate, Application, Interview, ApprovalRequest
from app.models.enums import UserRole, JobStatus, JobType, ApplicationStage, ApprovalStatus, ApprovalActionType, InterviewStatus
from app.core.security import hash_password

def seed_database():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        # Check if already seeded
        if db.query(User).filter(User.email == "admin@hirepilot.ai").first():
            print("Database already seeded.")
            return

        print("Seeding HirePilot AI database with realistic demo recruitment data...")

        # 1. Company
        company = Company(
            name="Acme Technologies",
            domain="acmetech.io"
        )
        db.add(company)
        db.commit()
        db.refresh(company)

        # 2. Users (Admin, HR Manager, Recruiter)
        admin = User(
            company_id=company.id,
            email="admin@hirepilot.ai",
            full_name="Sarah Jenkins",
            hashed_password=hash_password("admin123"),
            role=UserRole.ADMIN,
            is_active=True
        )
        hr_manager = User(
            company_id=company.id,
            email="hr@hirepilot.ai",
            full_name="Michael Scott",
            hashed_password=hash_password("hr123"),
            role=UserRole.HR_MANAGER,
            is_active=True
        )
        recruiter = User(
            company_id=company.id,
            email="recruiter@hirepilot.ai",
            full_name="Emily Davis",
            hashed_password=hash_password("recruiter123"),
            role=UserRole.RECRUITER,
            is_active=True
        )
        db.add_all([admin, hr_manager, recruiter])
        db.commit()

        # 3. Jobs
        job1 = Job(
            company_id=company.id,
            title="Senior Backend Engineer (Python / FastAPI)",
            department="Core Infrastructure",
            location="Remote",
            type=JobType.FULL_TIME,
            status=JobStatus.PUBLISHED,
            description="We are seeking an experienced Backend Engineer to scale our distributed cloud backend services.",
            requirements=["Python", "FastAPI", "PostgreSQL", "Docker", "Redis"],
            preferred_skills=["Kubernetes", "AWS", "LangGraph"],
            min_experience_years=4,
            salary_range="$140,000 - $175,000"
        )
        job2 = Job(
            company_id=company.id,
            title="Lead AI / ML Systems Engineer",
            department="AI Research",
            location="San Francisco, CA (Hybrid)",
            type=JobType.FULL_TIME,
            status=JobStatus.PUBLISHED,
            description="Build generative agentic workflows and LLM orchestration systems at scale.",
            requirements=["Python", "LangChain", "PyTorch", "FastAPI", "Vector DBs"],
            preferred_skills=["vLLM", "Triton", "Fine-tuning"],
            min_experience_years=5,
            salary_range="$170,000 - $210,000"
        )
        job3 = Job(
            company_id=company.id,
            title="Senior Frontend Engineer (React / TypeScript)",
            department="Design & UI Systems",
            location="Remote",
            type=JobType.FULL_TIME,
            status=JobStatus.DRAFT,
            description="Craft high-performance, polished web user interfaces and rich component libraries.",
            requirements=["React", "TypeScript", "Tailwind CSS", "Next.js"],
            preferred_skills=["Framer Motion", "GraphQL", "Shadcn UI"],
            min_experience_years=3,
            salary_range="$130,000 - $160,000"
        )
        db.add_all([job1, job2, job3])
        db.commit()
        db.refresh(job1)
        db.refresh(job2)
        db.refresh(job3)

        # 4. Candidates
        cand1 = Candidate(
            full_name="Alex Chen",
            email="alex.chen@example.com",
            phone="+1 (415) 555-0192",
            location="Seattle, WA",
            current_title="Senior Python Developer",
            experience_years=5.5,
            skills=["Python", "FastAPI", "PostgreSQL", "Docker", "Redis", "AWS"],
            notes="Strong distributed systems foundation, built high-throughput microservices."
        )
        cand2 = Candidate(
            full_name="Maya Patel",
            email="maya.patel@example.com",
            phone="+1 (650) 555-0143",
            location="San Francisco, CA",
            current_title="AI Research Engineer",
            experience_years=6.0,
            skills=["Python", "LangChain", "PyTorch", "FastAPI", "Machine Learning"],
            notes="Published research in multi-agent routing and tool integration."
        )
        cand3 = Candidate(
            full_name="Liam Gallagher",
            email="liam.g@example.com",
            phone="+1 (212) 555-0188",
            location="New York, NY",
            current_title="Full Stack Software Engineer",
            experience_years=3.5,
            skills=["React", "TypeScript", "Python", "Tailwind CSS"],
            notes="Excels in rapid prototyping and full stack feature delivery."
        )
        db.add_all([cand1, cand2, cand3])
        db.commit()
        db.refresh(cand1)
        db.refresh(cand2)
        db.refresh(cand3)

        # 5. Applications
        app1 = Application(
            job_id=job1.id,
            candidate_id=cand1.id,
            stage=ApplicationStage.SHORTLISTED,
            match_score=94.5
        )
        app2 = Application(
            job_id=job2.id,
            candidate_id=cand2.id,
            stage=ApplicationStage.INTERVIEW_SCHEDULED,
            match_score=96.0
        )
        app3 = Application(
            job_id=job1.id,
            candidate_id=cand3.id,
            stage=ApplicationStage.SCREENED,
            match_score=78.0
        )
        db.add_all([app1, app2, app3])
        db.commit()
        db.refresh(app1)
        db.refresh(app2)

        # 6. Scheduled Interview
        tomorrow = datetime.utcnow() + timedelta(days=1)
        interview1 = Interview(
            application_id=app2.id,
            interviewer_id=admin.id,
            title="AI Systems Architecture Interview with Maya Patel",
            scheduled_start=tomorrow.replace(hour=14, minute=0, second=0),
            scheduled_end=tomorrow.replace(hour=15, minute=0, second=0),
            meeting_link="https://meet.google.com/hpr-maya-ai",
            status=InterviewStatus.SCHEDULED,
            notes="Deep dive into multi-agent coordination and LLM reliability."
        )
        db.add(interview1)

        # 7. Pending Approvals (Human-in-the-Loop)
        approval1 = ApprovalRequest(
            action_type=ApprovalActionType.PUBLISH_JOB,
            status=ApprovalStatus.PENDING,
            requester_id=recruiter.id,
            title="Publish Job: Senior Frontend Engineer (React / TypeScript)",
            description="Requisition created by recruiter Emily Davis awaiting HR Manager approval to publish.",
            payload={"job_id": job3.id, "title": job3.title}
        )
        approval2 = ApprovalRequest(
            action_type=ApprovalActionType.SEND_EMAIL,
            status=ApprovalStatus.PENDING,
            requester_id=recruiter.id,
            title="Interview Invitation Email to Alex Chen",
            description="Technical round invitation drafted by AI Communication Agent for Senior Backend position.",
            payload={
                "recipient_email": "alex.chen@example.com",
                "subject": "Interview Invitation: Senior Backend Engineer at Acme Technologies",
                "body": "Dear Alex, We were thrilled by your profile and would love to schedule a technical round."
            }
        )
        db.add_all([approval1, approval2])
        db.commit()

        print("Database seed completed successfully with admin credentials: admin@hirepilot.ai / admin123")

if __name__ == "__main__":
    seed_database()
