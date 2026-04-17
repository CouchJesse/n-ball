from fastapi import Depends
from app.repositories.draw import DrawRepository
from app.schemas.check import CheckRequest, CheckResponse


class CheckService:
    def __init__(self, draw_repo: DrawRepository = Depends()):
        self.draw_repo = draw_repo

    def check_ticket(self, req: CheckRequest) -> CheckResponse:
        # Dummy logic
        return CheckResponse(prize_level=1, matched_reds=6, matched_blues=1)
