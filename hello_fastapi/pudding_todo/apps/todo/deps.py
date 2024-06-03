from typing import Annotated

from fastapi import Depends

from .services import TodoService


TodoServiceDep = Annotated[TodoService, Depends(TodoService)]
