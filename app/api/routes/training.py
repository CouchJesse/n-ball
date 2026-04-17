from fastapi import APIRouter, Depends
from app.schemas.training import TrainingCreate, TrainingResponse
from app.services.training import TrainingService
from pydantic import BaseModel

router = APIRouter()


class EvaluateRequest(BaseModel):
    training_id: int


@router.post("/create", response_model=TrainingResponse)
def create_training(req: TrainingCreate, training_service: TrainingService = Depends()):
    return training_service.create_training(req)


@router.post("/evaluate")
def evaluate_training(
    req: EvaluateRequest, training_service: TrainingService = Depends()
):
    return training_service.evaluate_training(req.training_id)
