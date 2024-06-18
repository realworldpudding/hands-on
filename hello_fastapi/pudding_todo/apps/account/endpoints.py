from fastapi import APIRouter, HTTPException, status, Response, Request

from pudding_todo.authentication import AuthBackendDep, CurrentUserDep, CurrentUserOptionalDep
from pudding_todo.templates import tpl

from .models import User
from .schemas import LoginSchema
from .deps import UserServiceDep

router = APIRouter()


@router.post("/login", name="login")
async def login(
        request: Request,
        payload: LoginSchema,
        service: UserServiceDep,
        auth_backend: AuthBackendDep,
    ) -> Response:
    user = await service.authenticate(payload.username, payload.password)
    if not user.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    strategy = auth_backend.get_strategy()
    response = await auth_backend.login(strategy, user)
    response.headers["HX-Redirect"] = str(request.url_for("list-todo-group-page"))
    return response


@router.get("/login", name="login-page")
@tpl.page("pages/login.jinja2")
async def login_page() -> dict:
    return {}


@router.get("/only-auth-user", name="only-auth-user", response_model=User)
async def only_auth_user(user: CurrentUserDep):
    return user


@router.get("/any-user", name="any-user")
async def any_user(user: CurrentUserOptionalDep) -> dict:
    if not user:
        return {"detail": "Anonymous"}
    return {"detail": "Authenticated"}
