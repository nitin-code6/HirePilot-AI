import pytest
from app.core.security import hash_password, verify_password, create_access_token, decode_token
from app.services.resume_parser import ResumeParserService
from app.services.screening_service import ScreeningEngine
from app.models.models import Job, Resume
from app.graph.supervisor import SupervisorOrchestrator

def test_password_hashing():
    pwd = "EnterprisePassword!99"
    hashed = hash_password(pwd)
    assert verify_password(pwd, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_jwt_token_lifecycle():
    payload = {"sub": "user_12345", "role": "admin"}
    token = create_access_token(payload)
    decoded = decode_token(token)
    assert decoded is not None
    assert decoded["sub"] == "user_12345"
    assert decoded["role"] == "admin"

def test_resume_parser_heuristics():
    sample_text = """
    Alex Johnson
    alex.johnson@example.com | (555) 234-5678
    Experienced Software Engineer with 6 years of experience in distributed cloud architectures.
    Skills: Python, FastAPI, PostgreSQL, Docker, Redis, Kubernetes, AWS.
    Education: B.S. in Computer Science.
    """
    parsed = ResumeParserService.parse_information(sample_text)
    assert parsed["email"] == "alex.johnson@example.com"
    assert parsed["experience_years"] == 6.0
    assert "Python" in parsed["skills"]
    assert "FastAPI" in parsed["skills"]

def test_deterministic_screening_engine():
    job = Job(
        title="Backend Engineer",
        requirements=["Python", "FastAPI", "PostgreSQL", "Docker"],
        preferred_skills=["Redis"],
        min_experience_years=4
    )
    resume = Resume(
        candidate_id="cand_1",
        filename="resume.pdf",
        file_path="/tmp/test.pdf",
        file_hash="abc",
        raw_text="Bachelor of Science in Computer Science",
        parsed_data={
            "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "Redis"],
            "experience_years": 5.0
        }
    )
    result = ScreeningEngine.match_resume_to_job(resume, job)
    assert result["overall_score"] > 85.0
    assert "python" in result["matching_skills"]
    assert len(result["missing_skills"]) == 0

def test_supervisor_routing():
    assert SupervisorOrchestrator.route_intent("Create a new Backend Engineer role") == "job_agent"
    assert SupervisorOrchestrator.route_intent("Screen the uploaded candidate resumes") == "resume_screening_agent"
    assert SupervisorOrchestrator.route_intent("Find available interview slots") == "interview_agent"
    assert SupervisorOrchestrator.route_intent("Draft an interview invitation email") == "communication_agent"
    assert SupervisorOrchestrator.route_intent("Show recruitment conversion funnel analytics") == "analytics_agent"
    assert SupervisorOrchestrator.route_intent("Find candidate profiles in talent pool") == "candidate_agent"
