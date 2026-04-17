from celery import Celery
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.task import Task
import time
import random

celery_app = Celery(
    "worker", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.task_routes = {"app.worker.crawler_task": "main-queue"}


def update_task_status(task_id: str, status: str, payload: dict = None):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.status = status
        if payload:
            task.payload = payload
        db.commit()
    db.close()


@celery_app.task(name="app.worker.crawler_task", bind=True)
def crawler_task(self, target_period: str, task_id: str):
    update_task_status(task_id, "running")
    # simulate crawler work
    time.sleep(2)
    # 模拟成功与失败（用于任务观测）
    if random.random() < 0.1:
        update_task_status(task_id, "failed", {"error": "Timeout"})
        raise Exception("Crawler timeout")

    update_task_status(
        task_id, "completed", {"result": f"Crawled period {target_period}"}
    )
    return {"status": "success", "period": target_period}


@celery_app.task(name="app.worker.training_evaluate_task", bind=True)
def training_evaluate_task(self, training_id: int):
    # Simulate async evaluate
    time.sleep(3)
    return {"training_id": training_id, "status": "evaluated"}


@celery_app.task(name="app.worker.iterate_algorithm_task", bind=True)
def iterate_algorithm_task(self, algo_id: int):
    # Simulate async iterate
    time.sleep(4)
    return {"algo_id": algo_id, "status": "iterated"}
