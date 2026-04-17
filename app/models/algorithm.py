from sqlalchemy import Column, Integer, String, JSON
from app.db.base import Base


class AlgorithmVersion(Base):
    __tablename__ = "algorithm_versions"
    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, unique=True, index=True)
    params_snapshot = Column(JSON)
    score = Column(Integer, default=0)
    data_range = Column(String)
    description = Column(String)
