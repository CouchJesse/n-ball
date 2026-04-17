from pydantic import BaseModel
from typing import List


class CheckRequest(BaseModel):
    ticket_reds: List[int]
    ticket_blues: List[int]
    period: str


class CheckResponse(BaseModel):
    prize_level: int
    matched_reds: int
    matched_blues: int
