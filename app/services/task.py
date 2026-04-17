from fastapi import Depends
from app.repositories.task import TaskRepository
from app.schemas.task import TaskTrigger
from app.worker import crawler_task


class TaskService:
    def __init__(self, task_repo: TaskRepository = Depends()):
        self.task_repo = task_repo

    def trigger_crawler_task(self, req: TaskTrigger):
        # 1. 存库
        task_id = self.task_repo.create_task("crawler", req.model_dump())
        # 2. 扔给 celery
        celery_task = crawler_task.delay(req.target_period, task_id)
        return {
            "task_id": str(task_id),
            "celery_id": celery_task.id,
            "status": "queued",
        }
