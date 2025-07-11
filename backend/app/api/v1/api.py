from fastapi import APIRouter
from app.api.v1.endpoints import fire_prediction, fire_simulation

api_router = APIRouter()

api_router.include_router(
    fire_prediction.router, 
    prefix="/fire-prediction", 
    tags=["fire-prediction"]
)

api_router.include_router(
    fire_simulation.router, 
    prefix="/fire-simulation", 
    tags=["fire-simulation"]
)
