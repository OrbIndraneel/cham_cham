from pydantic import BaseModel
from typing import List, Optional

class HazardPredictionRequest(BaseModel):
    latitude: float
    longitude: float
    rainfall_mm: float
    river_level_m: Optional[float] = None
    district_id: str

class HazardPredictionResponse(BaseModel):
    district_id: str
    primary_hazard: str
    secondary_cascade_hazard: str
    cascade_probability: float
    estimated_lead_time_mins: int
    risk_level: str  # High, Medium, Low
    polygon_coordinates: List[List[float]]

class EvacuationRouteRequest(BaseModel):
    user_lat: float
    user_lng: float
    destination_shelter_id: Optional[str] = None

class EvacuationRouteResponse(BaseModel):
    route_id: str
    distance_km: float
    estimated_time_mins: int
    hazard_avoided: bool
    route_coordinates: List[List[float]]
