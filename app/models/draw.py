from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Draw(Base):
    __tablename__ = "draws"
    id = Column(Integer, primary_key=True, index=True)
    period = Column(String, unique=True, index=True)
    reds = Column(String)
    blue = Column(Integer)
