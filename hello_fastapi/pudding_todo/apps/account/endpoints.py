from fastapi import APIRouter, HTTPException, status

from .models import User
from .schemas import LoginSchema
from .deps import UserServiceDep

router = APIRouter()


@router.post("/login", name="login")
async def login(payload: LoginSchema, service: UserServiceDep) -> User:
    user = await service.authenticate(payload.username, payload.password)
    if not user.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    return user
