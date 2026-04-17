from fastapi import Depends
from app.repositories.training import TrainingRepository
from app.schemas.training import TrainingCreate, TrainingResponse
from app.worker import training_evaluate_task


class TrainingService:
    def __init__(self, training_repo: TrainingRepository = Depends()):
        self.training_repo = training_repo

    def create_training(self, req: TrainingCreate) -> TrainingResponse:
        training = self.training_repo.create(req.name, req.config)
        return TrainingResponse(
            id=training.id, name=training.name, status=training.status
        )

    def evaluate_training(self, training_id: int):
        celery_task = training_evaluate_task.delay(training_id)
        return {
            "training_id": training_id,
            "task_id": celery_task.id,
            "status": "evaluating_queued",
        }
