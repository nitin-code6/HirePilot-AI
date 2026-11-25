from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.models import Interview, Application, User, AuditLog
from app.models.enums import InterviewStatus, UserRole
from app.schemas.recruitment import InterviewCreate, InterviewUpdate, InterviewResponse
from app.core.deps import get_current_user, RequireRole

router = APIRouter(prefix="/interviews", tags=["Interviews"])

@router.get("", response_model=List[InterviewResponse])
def list_interviews(
    application_id: Optional[str] = None,
    status: Optional[InterviewStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Interview)
    if application_id:
        query = query.filter(Interview.application_id == application_id)
    if status:
        query = query.filter(Interview.status == status)
    return query.order_by(Interview.scheduled_start.asc()).all()

@router.post("", response_model=InterviewResponse, status_code=status.HTTP_201_CREATED)
def create_interview(
    req: InterviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RequireRole([UserRole.ADMIN, UserRole.HR_MANAGER, UserRole.RECRUITER]))
):
    app = db.query(Application).filter(Application.id == req.application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    meeting_url = req.meeting_link or f"https://meet.google.com/hpr-{abs(hash(req.title)) % 10000}"
    interview = Interview(
        application_id=req.application_id,
        interviewer_id=req.interviewer_id or current_user.id,
        title=req.title,
        scheduled_start=req.scheduled_start,
        scheduled_end=req.scheduled_end,
        meeting_link=meeting_url,
        notes=req.notes,
        status=InterviewStatus.SCHEDULED
    )
    db.add(interview)
    db.commit()
    db.refresh(interview)
    return interview

@router.get("/{interview_id}", response_model=InterviewResponse)
def get_interview(interview_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview

@router.patch("/{interview_id}", response_model=InterviewResponse)
def update_interview(
    interview_id: str,
    req: InterviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RequireRole([UserRole.ADMIN, UserRole.HR_MANAGER, UserRole.RECRUITER]))
):
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
        
    update_data = req.model_dump(exclude_unset=True)
    for key, val in update_data.items():
        setattr(interview, key, val)
        
    db.commit()
    db.refresh(interview)
    return interview

@router.delete("/{interview_id}")
def delete_interview(
    interview_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(RequireRole([UserRole.ADMIN, UserRole.HR_MANAGER]))
):
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    db.delete(interview)
    db.commit()
    return {"message": "Interview cancelled successfully"}
