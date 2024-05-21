from fastapi import APIRouter, HTTPException, status, Depends

from .models import User
from .schemas import LoginSchema
from .services import UserService

router = APIRouter()


@router.post("/login", name="login")
async def login(payload: LoginSchema, service: UserService = Depends(UserService)) -> User:
    user = await service.authenticate(payload.username, payload.password)
    if not user.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    return user
