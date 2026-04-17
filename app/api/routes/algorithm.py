from fastapi import APIRouter, Depends
from app.schemas.algorithm import AlgorithmCreate, AlgorithmResponse
from app.services.algorithm import AlgorithmService
from pydantic import BaseModel

router = APIRouter()


class IterateRequest(BaseModel):
    algo_id: int


@router.post("/generate", response_model=AlgorithmResponse)
def generate_algorithm(
    req: AlgorithmCreate, algo_service: AlgorithmService = Depends()
):
    return algo_service.generate_algorithm(req)


@router.post("/iterate")
def iterate_algorithm(req: IterateRequest, algo_service: AlgorithmService = Depends()):
    return algo_service.iterate_algorithm(req.algo_id)
