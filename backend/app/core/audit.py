import datetime
from sqlalchemy.orm import Session
from app.models.models import AuditLog

class AuditLogger:
    @staticmethod
    def log(
        db: Session,
        action: str,
        entity_type: str,
        entity_id: str = None,
        user_id: str = None,
        details: dict = None
    ) -> AuditLog:
        record = AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details or {}
        )
        db.add(record)
        db.commit()
        return record
