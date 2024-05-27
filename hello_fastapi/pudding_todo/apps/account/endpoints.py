from fastapi import APIRouter, HTTPException, status, Response

from pudding_todo.authentication import AuthBackendDep
from .schemas import LoginSchema
from .deps import UserServiceDep

router = APIRouter()


@router.post("/login", name="login")
async def login(payload: LoginSchema, service: UserServiceDep, auth_backend: AuthBackendDep) -> Response:
    user = await service.authenticate(payload.username, payload.password)
    if not user.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    strategy = auth_backend.get_strategy()
    response = await auth_backend.login(strategy, user)
    return response
