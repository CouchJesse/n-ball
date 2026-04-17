from sqlalchemy import Column, Integer, String, JSON
from app.db.base import Base


class Training(Base):
    __tablename__ = "trainings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    status = Column(String)
    config = Column(JSON)
