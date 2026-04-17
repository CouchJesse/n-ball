from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.services.auth import AuthService

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, auth_service: AuthService = Depends()):
    return auth_service.register_user(user_in)


@router.post("/login")
def login(user_in: UserLogin, auth_service: AuthService = Depends()):
    return auth_service.authenticate(user_in)
