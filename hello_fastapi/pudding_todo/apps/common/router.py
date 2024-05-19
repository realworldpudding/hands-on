from fastapi import APIRouter
from .endpoints import router as common_router

router = APIRouter()
router.include_router(common_router)
