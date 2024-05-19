from fastapi import FastAPI
from pudding_todo.apps.common.router import router as common_router

app = FastAPI()
app.include_router(common_router)
