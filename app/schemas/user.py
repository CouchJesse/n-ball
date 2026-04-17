from pydantic import BaseModel, Field, ConfigDict


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    invite_code: str = Field(..., description="邀请码")


class UserLogin(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
