from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.models import ApprovalRequest, User, Job, Interview, Application, EmailLog, AuditLog
from app.models.enums import ApprovalStatus, ApprovalActionType, JobStatus, UserRole, InterviewStatus
from app.schemas.recruitment import ApprovalResponse, ApprovalReviewRequest
from app.integrations.providers import EmailService, CalendarService
from app.core.deps import get_current_user, RequireRole

router = APIRouter(prefix="/approvals", tags=["Approvals"])

@router.get("", response_model=List[ApprovalResponse])
def list_approvals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(ApprovalRequest).order_by(ApprovalRequest.created_at.desc()).all()

@router.post("/{approval_id}/approve", response_model=ApprovalResponse)
def approve_request(
    approval_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(RequireRole([UserRole.ADMIN, UserRole.HR_MANAGER]))
):
    approval = db.query(ApprovalRequest).filter(ApprovalRequest.id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval request not found")
    if approval.status != ApprovalStatus.PENDING:
        raise HTTPException(status_code=400, detail="Approval request is not pending")

    # Enforce action execution on approval
    payload = approval.payload or {}
    result_log = {}

    if approval.action_type == ApprovalActionType.PUBLISH_JOB:
        job_id = payload.get("job_id")
        job = db.query(Job).filter(Job.id == job_id).first()
        if job:
            job.status = JobStatus.PUBLISHED
            result_log = {"action": "job_published", "job_id": job.id, "title": job.title}
            
    elif approval.action_type == ApprovalActionType.SEND_EMAIL:
        res = EmailService.send_email(
            to_email=payload.get("recipient_email"),
            subject=payload.get("subject"),
            body=payload.get("body")
        )
        email_record = EmailLog(
            recipient_email=payload.get("recipient_email"),
            subject=payload.get("subject"),
            body=payload.get("body"),
            status=res["status"]
        )
        db.add(email_record)
        result_log = res

    elif approval.action_type == ApprovalActionType.SCHEDULE_INTERVIEW:
        cal_res = CalendarService.create_meeting(
            title=payload.get("meeting_title", "Technical Interview"),
            start_time=payload.get("slot"),
            end_time=payload.get("slot"),
            attendee_email="candidate@example.com"
        )
        result_log = cal_res

    approval.status = ApprovalStatus.APPROVED
    approval.reviewer_id = current_user.id
    approval.result_log = result_log

    audit = AuditLog(
        user_id=current_user.id,
        action="APPROVE_REQUEST",
        entity_type="APPROVAL_REQUEST",
        entity_id=approval.id,
        details={"action_type": approval.action_type.value, "result": result_log}
    )
    db.add(audit)
    db.commit()
    db.refresh(approval)
    return approval

@router.post("/{approval_id}/reject", response_model=ApprovalResponse)
def reject_request(
    approval_id: str,
    req: ApprovalReviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(RequireRole([UserRole.ADMIN, UserRole.HR_MANAGER]))
):
    approval = db.query(ApprovalRequest).filter(ApprovalRequest.id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval request not found")
    if approval.status != ApprovalStatus.PENDING:
        raise HTTPException(status_code=400, detail="Approval request is not pending")

    approval.status = ApprovalStatus.REJECTED
    approval.reviewer_id = current_user.id
    approval.rejection_reason = req.reason or "Rejected by HR Manager"

    audit = AuditLog(
        user_id=current_user.id,
        action="REJECT_REQUEST",
        entity_type="APPROVAL_REQUEST",
        entity_id=approval.id,
        details={"reason": approval.rejection_reason}
    )
    db.add(audit)
    db.commit()
    db.refresh(approval)
    return approval
