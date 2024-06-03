from typing import Annotated

from fastapi import Depends

from .services import TodoGroupService, TodoService


TodoGroupServiceDep = Annotated[TodoGroupService, Depends(TodoGroupService)]

TodoServiceDep = Annotated[TodoService, Depends(TodoService)]
