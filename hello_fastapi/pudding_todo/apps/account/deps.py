from typing import Annotated

from fastapi import Depends

from .services import UserService

UserServiceDep = Annotated[UserService, Depends(UserService)]
