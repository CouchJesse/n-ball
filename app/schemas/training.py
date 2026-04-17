from pydantic import BaseModel


class TrainingCreate(BaseModel):
    name: str
    config: dict


class TrainingResponse(BaseModel):
    id: int
    name: str
    status: str
