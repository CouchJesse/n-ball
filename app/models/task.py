from sqlalchemy import Column, Integer, String, JSON
from app.db.base import Base


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(String)
    status = Column(String)
    payload = Column(JSON)
