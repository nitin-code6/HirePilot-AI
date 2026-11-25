import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Boolean, Integer, Float, DateTime, ForeignKey, Enum as SQLEnum, JSON
)
from sqlalchemy.orm import relationship
from app.database.session import Base
from app.models.enums import (
    UserRole, JobStatus, JobType, ApplicationStage, ApprovalStatus, ApprovalActionType, InterviewStatus
)

def generate_uuid():
    return str(uuid.uuid4())

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    domain = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    users = relationship("User", back_populates="company", cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="company", cascade="all, delete-orphan")

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.RECRUITER, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    company = relationship("Company", back_populates="users")
    interviews = relationship("Interview", back_populates="interviewer")
    approvals_requested = relationship("ApprovalRequest", foreign_keys="ApprovalRequest.requester_id", back_populates="requester")
    approvals_reviewed = relationship("ApprovalRequest", foreign_keys="ApprovalRequest.reviewer_id", back_populates="reviewer")

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=True)
    title = Column(String(255), index=True, nullable=False)
    department = Column(String(100), nullable=True)
    location = Column(String(100), default="Remote")
    type = Column(SQLEnum(JobType), default=JobType.FULL_TIME)
    status = Column(SQLEnum(JobStatus), default=JobStatus.DRAFT, index=True)
    description = Column(Text, nullable=False)
    requirements = Column(JSON, default=list) # List of required strings/skills
    preferred_skills = Column(JSON, default=list)
    min_experience_years = Column(Integer, default=0)
    salary_range = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    company = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    location = Column(String(100), nullable=True)
    current_title = Column(String(255), nullable=True)
    experience_years = Column(Float, default=0.0)
    skills = Column(JSON, default=list)
    linkedin_url = Column(String(255), nullable=True)
    github_url = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    resumes = relationship("Resume", back_populates="candidate", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="candidate", cascade="all, delete-orphan")

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    candidate_id = Column(String(36), ForeignKey("candidates.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_hash = Column(String(64), index=True, nullable=False) # SHA-256 for dedup
    raw_text = Column(Text, nullable=True)
    parsed_data = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    candidate = relationship("Candidate", back_populates="resumes")
    screening_reports = relationship("ScreeningReport", back_populates="resume", cascade="all, delete-orphan")

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    job_id = Column(String(36), ForeignKey("jobs.id"), nullable=False)
    candidate_id = Column(String(36), ForeignKey("candidates.id"), nullable=False)
    stage = Column(SQLEnum(ApplicationStage), default=ApplicationStage.APPLIED, index=True)
    match_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    job = relationship("Job", back_populates="applications")
    candidate = relationship("Candidate", back_populates="applications")
    interviews = relationship("Interview", back_populates="application", cascade="all, delete-orphan")

class ScreeningReport(Base):
    __tablename__ = "screening_reports"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    resume_id = Column(String(36), ForeignKey("resumes.id"), nullable=False)
    job_id = Column(String(36), ForeignKey("jobs.id"), nullable=False)
    overall_score = Column(Float, nullable=False) # 0 to 100
    skills_score = Column(Float, nullable=False)
    experience_score = Column(Float, nullable=False)
    education_score = Column(Float, nullable=False)
    matching_skills = Column(JSON, default=list)
    missing_skills = Column(JSON, default=list)
    strengths = Column(JSON, default=list)
    weaknesses = Column(JSON, default=list)
    explanation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    resume = relationship("Resume", back_populates="screening_reports")

class Interview(Base):
    __tablename__ = "interviews"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    application_id = Column(String(36), ForeignKey("applications.id"), nullable=False)
    interviewer_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    title = Column(String(255), nullable=False)
    scheduled_start = Column(DateTime, nullable=False)
    scheduled_end = Column(DateTime, nullable=False)
    meeting_link = Column(String(500), nullable=True)
    status = Column(SQLEnum(InterviewStatus), default=InterviewStatus.SCHEDULED)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    application = relationship("Application", back_populates="interviews")
    interviewer = relationship("User", back_populates="interviews")
    feedback = relationship("InterviewFeedback", back_populates="interview", uselist=False, cascade="all, delete-orphan")

class InterviewFeedback(Base):
    __tablename__ = "interview_feedbacks"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    interview_id = Column(String(36), ForeignKey("interviews.id"), unique=True, nullable=False)
    rating = Column(Integer, nullable=False) # 1-5
    strengths = Column(Text, nullable=True)
    weaknesses = Column(Text, nullable=True)
    recommendation = Column(String(50), nullable=False) # Hire / No Hire / Strong Hire
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    interview = relationship("Interview", back_populates="feedback")

class ApprovalRequest(Base):
    __tablename__ = "approval_requests"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    action_type = Column(SQLEnum(ApprovalActionType), nullable=False)
    status = Column(SQLEnum(ApprovalStatus), default=ApprovalStatus.PENDING, index=True)
    requester_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    reviewer_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    payload = Column(JSON, default=dict) # Details needed to execute action on approval
    result_log = Column(JSON, nullable=True) # Execution outcome details
    rejection_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    requester = relationship("User", foreign_keys=[requester_id], back_populates="approvals_requested")
    reviewer = relationship("User", foreign_keys=[reviewer_id], back_populates="approvals_reviewed")

class EmailLog(Base):
    __tablename__ = "email_logs"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    recipient_email = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    status = Column(String(50), default="sent") # sent / failed / mock
    sent_at = Column(DateTime, default=datetime.utcnow)

class ConversationSession(Base):
    __tablename__ = "conversation_sessions"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), default="New Recruitment Session")
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    messages = relationship("ConversationMessage", back_populates="session", cascade="all, delete-orphan", order_by="ConversationMessage.created_at")

class ConversationMessage(Base):
    __tablename__ = "conversation_messages"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    session_id = Column(String(36), ForeignKey("conversation_sessions.id"), nullable=False)
    role = Column(String(50), nullable=False) # user / assistant / system / agent / tool
    content = Column(Text, nullable=False)
    agent_name = Column(String(100), nullable=True) # which agent answered
    metadata_json = Column(JSON, nullable=True) # UI cards, structured artifacts
    created_at = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("ConversationSession", back_populates="messages")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), nullable=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(100), nullable=False)
    entity_id = Column(String(36), nullable=True)
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
