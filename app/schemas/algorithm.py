from pydantic import BaseModel


class AlgorithmCreate(BaseModel):
    name: str
    params_snapshot: dict


class AlgorithmResponse(BaseModel):
    id: int
    version: str
