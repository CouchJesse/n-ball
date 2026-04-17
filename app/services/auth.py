from fastapi import Depends
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserLogin, UserResponse


class AuthService:
    def __init__(self, user_repo: UserRepository = Depends()):
        self.user_repo = user_repo

    def register_user(self, user_in: UserCreate) -> UserResponse:
        # Dummy response
        return UserResponse(id=1, username=user_in.username)

    def authenticate(self, user_in: UserLogin):
        return {"access_token": "dummy_token", "token_type": "bearer"}
