from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import SessionLocal
from app.models.algorithm import AlgorithmVersion


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class AlgorithmRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_version(self, name: str, params: dict):
        algo = AlgorithmVersion(version=f"v1.{name}", params_snapshot=params)
        self.db.add(algo)
        self.db.commit()
        self.db.refresh(algo)
        return algo
