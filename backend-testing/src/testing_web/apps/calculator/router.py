from fastapi import APIRouter

from .endpoints import router as calculator_router

router = APIRouter(prefix="/calculator")

router.include_router(calculator_router)
