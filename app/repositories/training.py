from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import SessionLocal
from app.models.training import Training


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TrainingRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create(self, name: str, config: dict):
        training = Training(name=name, config=config, status="pending")
        self.db.add(training)
        self.db.commit()
        self.db.refresh(training)
        return training
