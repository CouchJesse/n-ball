from fastapi import APIRouter, Depends
from app.schemas.task import TaskTrigger
from app.services.task import TaskService

router = APIRouter()


@router.post("/start")
def start_crawler(req: TaskTrigger, task_service: TaskService = Depends()):
    return task_service.trigger_crawler_task(req)
