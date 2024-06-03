from fastapi import APIRouter

from .endpoints import router as todo_router
router = APIRouter()

router.include_router(todo_router)

