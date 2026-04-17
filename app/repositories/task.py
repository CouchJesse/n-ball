from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import SessionLocal
from app.models.task import Task


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TaskRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_task(self, task_type: str, payload: dict) -> int:
        db_task = Task(task_type=task_type, status="pending", payload=payload)
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task.id
