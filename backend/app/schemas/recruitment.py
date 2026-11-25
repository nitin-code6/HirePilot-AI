from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, EmailStr, Field
from app.models.enums import (
    UserRole, JobStatus, JobType, ApplicationStage, ApprovalStatus, ApprovalActionType, InterviewStatus
)

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.RECRUITER
    company_id: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None
    role: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

# Job schemas
class JobBase(BaseModel):
    title: str
    department: Optional[str] = None
    location: Optional[str] = "Remote"
    type: JobType = JobType.FULL_TIME
    description: str
    requirements: List[str] = []
    preferred_skills: List[str] = []
    min_experience_years: int = 0
    salary_range: Optional[str] = None

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    type: Optional[JobType] = None
    status: Optional[JobStatus] = None
    description: Optional[str] = None
    requirements: Optional[List[str]] = None
    preferred_skills: Optional[List[str]] = None
    min_experience_years: Optional[int] = None
    salary_range: Optional[str] = None

class JobResponse(JobBase):
    id: str
    status: JobStatus
    created_at: datetime
    updated_at: datetime
    applications_count: Optional[int] = 0
    
    class Config:
        from_attributes = True

# Candidate schemas
class CandidateBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    location: Optional[str] = None
    current_title: Optional[str] = None
    experience_years: float = 0.0
    skills: List[str] = []
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    notes: Optional[str] = None

class CandidateCreate(CandidateBase):
    pass

class CandidateUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    current_title: Optional[str] = None
    experience_years: Optional[float] = None
    skills: Optional[List[str]] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    notes: Optional[str] = None

class CandidateResponse(CandidateBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Resume schemas
class ResumeResponse(BaseModel):
    id: str
    candidate_id: str
    filename: str
    file_hash: str
    parsed_data: Dict[str, Any] = {}
    created_at: datetime

    class Config:
        from_attributes = True

# Application schemas
class ApplicationCreate(BaseModel):
    job_id: str
    candidate_id: str
    stage: ApplicationStage = ApplicationStage.APPLIED

class ApplicationUpdate(BaseModel):
    stage: ApplicationStage

class ApplicationResponse(BaseModel):
    id: str
    job_id: str
    candidate_id: str
    stage: ApplicationStage
    match_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    candidate: Optional[CandidateResponse] = None
    job: Optional[JobResponse] = None

    class Config:
        from_attributes = True

# Screening schemas
class ScreeningReportResponse(BaseModel):
    id: str
    resume_id: str
    job_id: str
    overall_score: float
    skills_score: float
    experience_score: float
    education_score: float
    matching_skills: List[str]
    missing_skills: List[str]
    strengths: List[str]
    weaknesses: List[str]
    explanation: str
    created_at: datetime

    class Config:
        from_attributes = True

# Interview schemas
class InterviewCreate(BaseModel):
    application_id: str
    interviewer_id: Optional[str] = None
    title: str
    scheduled_start: datetime
    scheduled_end: datetime
    meeting_link: Optional[str] = None
    notes: Optional[str] = None

class InterviewUpdate(BaseModel):
    title: Optional[str] = None
    interviewer_id: Optional[str] = None
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    meeting_link: Optional[str] = None
    status: Optional[InterviewStatus] = None
    notes: Optional[str] = None

class InterviewResponse(BaseModel):
    id: str
    application_id: str
    interviewer_id: Optional[str] = None
    title: str
    scheduled_start: datetime
    scheduled_end: datetime
    meeting_link: Optional[str] = None
    status: InterviewStatus
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Approval schemas
class ApprovalCreate(BaseModel):
    action_type: ApprovalActionType
    title: str
    description: str
    payload: Dict[str, Any]

class ApprovalReviewRequest(BaseModel):
    reason: Optional[str] = None

class ApprovalResponse(BaseModel):
    id: str
    action_type: ApprovalActionType
    status: ApprovalStatus
    requester_id: Optional[str] = None
    reviewer_id: Optional[str] = None
    title: str
    description: str
    payload: Dict[str, Any]
    result_log: Optional[Dict[str, Any]] = None
    rejection_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Assistant Chat schemas
class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    session_id: str
    reply: str
    agent_used: Optional[str] = None
    action_required: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
