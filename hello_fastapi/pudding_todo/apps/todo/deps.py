from typing import Annotated

from fastapi import Depends

from .services import TodoGroupService, TodoService, AttachmentService


TodoGroupServiceDep = Annotated[TodoGroupService, Depends(TodoGroupService)]

TodoServiceDep = Annotated[TodoService, Depends(TodoService)]

AttachmentServiceDep = Annotated[AttachmentService, Depends(AttachmentService)]
