from app.api.routes.experiments import router as experiment_router

from fastapi import FastAPI

app = FastAPI()
app.include_router(experiment_router)