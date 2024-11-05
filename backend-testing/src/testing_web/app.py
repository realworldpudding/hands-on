from fastapi import FastAPI

from .apps.calculator.router import router as calculator_router

app = FastAPI()

app.include_router(calculator_router)
