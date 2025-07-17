from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CoordinateInput(BaseModel):
    latitude: float
    longitude: float

class WeatherData(BaseModel):
    temperature: float
    humidity: float
    wind_speed: float
    wind_direction: float
    rainfall: float

class FirePredictionRequest(BaseModel):
    region_bounds: List[CoordinateInput]  # Bounding box
    weather_data: WeatherData
    prediction_date: datetime

class FirePredictionResponse(BaseModel):
    prediction_map_url: str
    risk_zones: List[dict]
    overall_risk_level: str
    confidence_score: float
