from fastapi import APIRouter, Depends
from app.schemas.check import CheckRequest, CheckResponse
from app.services.check import CheckService

router = APIRouter()


@router.post("/draw", response_model=CheckResponse)
def check_draw(req: CheckRequest, check_service: CheckService = Depends()):
    return check_service.check_ticket(req)
