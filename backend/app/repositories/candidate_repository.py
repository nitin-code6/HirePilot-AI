from sqlalchemy.orm import Session
from app.models.models import Candidate
from typing import List, Optional

class CandidateRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, candidate_id: str) -> Optional[Candidate]:
        return self.db.query(Candidate).filter(Candidate.id == candidate_id).first()

    def get_by_email(self, email: str) -> Optional[Candidate]:
        return self.db.query(Candidate).filter(Candidate.email == email.lower()).first()

    def list_all(self, skip: int = 0, limit: int = 50) -> List[Candidate]:
        return self.db.query(Candidate).order_by(Candidate.created_at.desc()).offset(skip).limit(limit).all()
