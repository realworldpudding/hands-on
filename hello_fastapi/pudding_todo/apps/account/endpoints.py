from fastapi import APIRouter, HTTPException, status, Response

from pudding_todo.authentication import AuthBackendDep, CurrentUserDep, CurrentUserOptionalDep

from .models import User
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


@router.get("/only-auth-user", name="only-auth-user", response_model=User)
async def only_auth_user(user: CurrentUserDep):
    return user


@router.get("/any-user", name="any-user")
async def any_user(user: CurrentUserOptionalDep) -> dict:
    if not user:
        return {"detail": "Anonymous"}
    return {"detail": "Authenticated"}
