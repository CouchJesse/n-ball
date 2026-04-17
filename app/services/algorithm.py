from fastapi import Depends
from app.repositories.algorithm import AlgorithmRepository
from app.schemas.algorithm import AlgorithmCreate, AlgorithmResponse
from app.worker import iterate_algorithm_task


class AlgorithmService:
    def __init__(self, algo_repo: AlgorithmRepository = Depends()):
        self.algo_repo = algo_repo

    def generate_algorithm(self, req: AlgorithmCreate) -> AlgorithmResponse:
        algo = self.algo_repo.create_version(req.name, req.params_snapshot)
        return AlgorithmResponse(id=algo.id, version=algo.version)

    def iterate_algorithm(self, algo_id: int):
        celery_task = iterate_algorithm_task.delay(algo_id)
        return {
            "algo_id": algo_id,
            "task_id": celery_task.id,
            "status": "iterate_queued",
        }
