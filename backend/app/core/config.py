from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Forest Fire Prediction API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # ML Model paths
    FIRE_PREDICTION_MODEL_PATH: str = "models/fire_prediction_model.h5"
    SIMULATION_MODEL_PATH: str = "models/simulation_model.pkl"
    
    # Data paths
    DATA_DIR: str = "data"
    RASTER_OUTPUT_DIR: str = "outputs/rasters"
    
    # External API keys (if needed)
    WEATHER_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()
