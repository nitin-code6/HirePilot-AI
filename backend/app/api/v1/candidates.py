from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.models import Candidate, Application, Resume, AuditLog
from app.models.enums import UserRole
from app.schemas.recruitment import (
    CandidateCreate, CandidateUpdate, CandidateResponse,
    ApplicationCreate, ApplicationUpdate, ApplicationResponse
)
from app.core.deps import get_current_user, RequireRole

router = APIRouter(tags=["Candidates & Applications"])

# Candidate routes
@router.get("/candidates", response_model=List[CandidateResponse])
def list_candidates(
    search: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Candidate)
    if search:
        query = query.filter(
            Candidate.full_name.ilike(f"%{search}%") |
            Candidate.email.ilike(f"%{search}%") |
            Candidate.current_title.ilike(f"%{search}%")
        )
    return query.order_by(Candidate.created_at.desc()).offset(skip).limit(limit).all()

@router.post("/candidates", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
def create_candidate(
    req: CandidateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RequireRole([UserRole.ADMIN, UserRole.HR_MANAGER, UserRole.RECRUITER]))
):
    existing = db.query(Candidate).filter(Candidate.email == req.email.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Candidate with this email already exists")
        
    candidate = Candidate(
        email=req.email.lower(),
        full_name=req.full_name,
        phone=req.phone,
        location=req.location,
        current_title=req.current_title,
        experience_years=req.experience_years,
        skills=req.skills,
        linkedin_url=req.linkedin_url,
        github_url=req.github_url,
        notes=req.notes
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate

@router.get("/candidates/{candidate_id}", response_model=CandidateResponse)
def get_candidate(candidate_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate

@router.patch("/candidates/{candidate_id}", response_model=CandidateResponse)
def update_candidate(
    candidate_id: str,
    req: CandidateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RequireRole([UserRole.ADMIN, UserRole.HR_MANAGER, UserRole.RECRUITER]))
):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
        
    update_data = req.model_dump(exclude_unset=True)
    for key, val in update_data.items():
        setattr(candidate, key, val)
        
    db.commit()
    db.refresh(candidate)
    return candidate

# Application routes
@router.get("/applications", response_model=List[ApplicationResponse])
def list_applications(
    job_id: Optional[str] = None,
    candidate_id: Optional[str] = None,
    stage: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Application)
    if job_id:
        query = query.filter(Application.job_id == job_id)
    if candidate_id:
        query = query.filter(Application.candidate_id == candidate_id)
    if stage:
        query = query.filter(Application.stage == stage)
    return query.order_by(Application.created_at.desc()).all()

@router.post("/applications", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(
    req: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RequireRole([UserRole.ADMIN, UserRole.HR_MANAGER, UserRole.RECRUITER]))
):
    app = Application(
        job_id=req.job_id,
        candidate_id=req.candidate_id,
        stage=req.stage
    )
    db.add(app)
    db.commit()
    db.refresh(app)
    return app

@router.patch("/applications/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: str,
    req: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RequireRole([UserRole.ADMIN, UserRole.HR_MANAGER, UserRole.RECRUITER]))
):
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
        
    app.stage = req.stage
    db.commit()
    db.refresh(app)
    return app
