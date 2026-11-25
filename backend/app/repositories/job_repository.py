from sqlalchemy.orm import Session
from app.models.models import Job
from typing import List, Optional

class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, job_id: str) -> Optional[Job]:
        return self.db.query(Job).filter(Job.id == job_id).first()

    def list_all(self, skip: int = 0, limit: int = 50) -> List[Job]:
        return self.db.query(Job).order_by(Job.created_at.desc()).offset(skip).limit(limit).all()

    def create(self, **kwargs) -> Job:
        job = Job(**kwargs)
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job
