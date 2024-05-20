from fastapi import APIRouter

from .endpoints import router as account_router
router = APIRouter()

router.include_router(account_router)
