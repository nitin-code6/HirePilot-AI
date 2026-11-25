from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.models import Job, User, Application, AuditLog
from app.models.enums import JobStatus, UserRole
from app.schemas.recruitment import JobCreate, JobUpdate, JobResponse
from app.core.deps import get_current_user, RequireRole

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.get("", response_model=List[JobResponse])
def list_jobs(
    status: Optional[JobStatus] = None,
    department: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Job)
    if status:
        query = query.filter(Job.status == status)
    if department:
        query = query.filter(Job.department.ilike(f"%{department}%"))
    if search:
        query = query.filter(Job.title.ilike(f"%{search}%") | Job.description.ilike(f"%{search}%"))
        
    jobs = query.order_by(Job.created_at.desc()).offset(skip).limit(limit).all()
    
    # Enrich with application counts
    result = []
    for j in jobs:
        count = db.query(Application).filter(Application.job_id == j.id).count()
        resp = JobResponse.model_validate(j)
        resp.applications_count = count
        result.append(resp)
    return result

@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(
    req: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RequireRole([UserRole.ADMIN, UserRole.HR_MANAGER, UserRole.RECRUITER]))
):
    job = Job(
        company_id=current_user.company_id,
        title=req.title,
        department=req.department,
        location=req.location,
        type=req.type,
        status=JobStatus.DRAFT,
        description=req.description,
        requirements=req.requirements,
        preferred_skills=req.preferred_skills,
        min_experience_years=req.min_experience_years,
        salary_range=req.salary_range
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    
    audit = AuditLog(
        user_id=current_user.id,
        action="CREATE_JOB",
        entity_type="JOB",
        entity_id=job.id,
        details={"title": job.title}
    )
    db.add(audit)
    db.commit()
    
    resp = JobResponse.model_validate(job)
    resp.applications_count = 0
    return resp

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    count = db.query(Application).filter(Application.job_id == job.id).count()
    resp = JobResponse.model_validate(job)
    resp.applications_count = count
    return resp

@router.patch("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: str,
    req: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RequireRole([UserRole.ADMIN, UserRole.HR_MANAGER, UserRole.RECRUITER]))
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    update_data = req.model_dump(exclude_unset=True)
    for key, val in update_data.items():
        setattr(job, key, val)
        
    db.commit()
    db.refresh(job)
    
    audit = AuditLog(
        user_id=current_user.id,
        action="UPDATE_JOB",
        entity_type="JOB",
        entity_id=job.id,
        details={"updated_fields": list(update_data.keys())}
    )
    db.add(audit)
    db.commit()
    
    count = db.query(Application).filter(Application.job_id == job.id).count()
    resp = JobResponse.model_validate(job)
    resp.applications_count = count
    return resp

@router.delete("/{job_id}")
def delete_job(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(RequireRole([UserRole.ADMIN, UserRole.HR_MANAGER]))
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    db.delete(job)
    db.commit()
    return {"message": "Job deleted successfully"}
