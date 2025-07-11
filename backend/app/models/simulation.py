from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime

class SimulationRequest(BaseModel):
    fire_origin_points: List[CoordinateInput]
    simulation_hours: List[int]  # [1, 2, 3, 6, 12]
    weather_conditions: WeatherData
    terrain_data: Optional[Dict] = None

class SimulationResponse(BaseModel):
    simulation_id: str
    animation_url: str
    hourly_spread_maps: Dict[int, str]  # hour -> raster_url
    affected_area_stats: Dict[int, float]  # hour -> area_in_hectares
