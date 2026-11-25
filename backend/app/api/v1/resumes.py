import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.models import Resume, Candidate, Job, Application, ScreeningReport, AuditLog
from app.models.enums import UserRole, ApplicationStage
from app.schemas.recruitment import ResumeResponse, ScreeningReportResponse
from app.services.resume_parser import ResumeParserService
from app.services.screening_service import ScreeningEngine
from app.core.config import settings
from app.core.deps import get_current_user, RequireRole

router = APIRouter(prefix="/resumes", tags=["Resumes & Screening"])

@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    candidate_id: str = Form(None),
    job_id: str = Form(None),
    db: Session = Depends(get_db),
    current_user = Depends(RequireRole([UserRole.ADMIN, UserRole.HR_MANAGER, UserRole.RECRUITER]))
):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".docx", ".doc", ".txt"]:
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload PDF, DOCX, or TXT.")

    file_bytes = await file.read()
    if len(file_bytes) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File exceeds maximum size of {settings.MAX_UPLOAD_SIZE_MB}MB")

    file_hash = ResumeParserService.calculate_sha256(file_bytes)
    
    # Save file securely
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    saved_filename = f"{file_hash[:16]}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, saved_filename)
    
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    # Extract text and parse
    raw_text = ResumeParserService.extract_text(file_path)
    parsed_info = ResumeParserService.parse_information(raw_text)

    # Resolve or create candidate
    if not candidate_id:
        cand_email = parsed_info.get("email") or f"candidate_{file_hash[:8]}@example.com"
        cand = db.query(Candidate).filter(Candidate.email == cand_email).first()
        if not cand:
            cand = Candidate(
                email=cand_email,
                full_name=parsed_info.get("full_name") or "Applicant",
                phone=parsed_info.get("phone"),
                experience_years=parsed_info.get("experience_years", 0.0),
                skills=parsed_info.get("skills", [])
            )
            db.add(cand)
            db.commit()
            db.refresh(cand)
        candidate_id = cand.id

    resume = Resume(
        candidate_id=candidate_id,
        filename=file.filename,
        file_path=file_path,
        file_hash=file_hash,
        raw_text=raw_text,
        parsed_data=parsed_info
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    # If job_id provided, create application & auto-screen
    if job_id:
        job = db.query(Job).filter(Job.id == job_id).first()
        if job:
            app = db.query(Application).filter(Application.job_id == job_id, Application.candidate_id == candidate_id).first()
            if not app:
                app = Application(job_id=job_id, candidate_id=candidate_id, stage=ApplicationStage.SCREENED)
                db.add(app)
            
            # Execute screening
            report_data = ScreeningEngine.match_resume_to_job(resume, job)
            report = ScreeningReport(
                resume_id=resume.id,
                job_id=job.id,
                **report_data
            )
            db.add(report)
            app.match_score = report_data["overall_score"]
            db.commit()

    return resume

@router.post("/{resume_id}/screen", response_model=ScreeningReportResponse)
def screen_resume(
    resume_id: str,
    job_id: str = Form(...),
    db: Session = Depends(get_db),
    current_user = Depends(RequireRole([UserRole.ADMIN, UserRole.HR_MANAGER, UserRole.RECRUITER]))
):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    report_data = ScreeningEngine.match_resume_to_job(resume, job)
    report = ScreeningReport(
        resume_id=resume.id,
        job_id=job.id,
        **report_data
    )
    db.add(report)
    
    app = db.query(Application).filter(Application.job_id == job_id, Application.candidate_id == resume.candidate_id).first()
    if app:
        app.match_score = report_data["overall_score"]
        app.stage = ApplicationStage.SCREENED
        
    db.commit()
    db.refresh(report)
    return report

@router.get("/{resume_id}/report", response_model=ScreeningReportResponse)
def get_report(resume_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    report = db.query(ScreeningReport).filter(ScreeningReport.resume_id == resume_id).order_by(ScreeningReport.created_at.desc()).first()
    if not report:
        raise HTTPException(status_code=404, detail="Screening report not found")
    return report
