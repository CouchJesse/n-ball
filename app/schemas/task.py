from pydantic import BaseModel


class TaskTrigger(BaseModel):
    target_period: str
