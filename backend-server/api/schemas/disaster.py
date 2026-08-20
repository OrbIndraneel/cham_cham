from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ShelterSchema(BaseModel):
    shelter_id: str
    name: str
    latitude: float
    longitude: float
    capacity: int
    current_occupancy: int
    status: str
    address: Optional[str] = None
    contact: Optional[str] = None
    distance_km: Optional[float] = None
    medical_facilities_available: Optional[bool] = True
    food_supplies_days: Optional[int] = 7
    power_generator: Optional[bool] = True
    helipad_access: Optional[bool] = False
    water_supply_liters: Optional[int] = 5000
    admin_incharge_name: Optional[str] = None
    admin_incharge_phone: Optional[str] = None

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
    affected_population_estimate: Optional[int] = 0
    severity_score: Optional[float] = 5.0
    soil_saturation_index: Optional[float] = 0.0
    polygon_coordinates: List[List[float]]

class EvacuationRouteRequest(BaseModel):
    user_lat: float
    user_lng: float
    user_id: Optional[str] = None
    transport_mode: Optional[str] = "walking"
    destination_shelter_id: Optional[str] = None

class EvacuationRouteResponse(BaseModel):
    route_id: str
    distance_km: float
    estimated_time_mins: int
    hazard_avoided: bool
    transport_mode: Optional[str] = "walking"
    route_coordinates: List[List[float]]

class SOSAlertRequest(BaseModel):
    user_id: str
    user_name: Optional[str] = "Anonymous"
    user_phone: Optional[str] = "N/A"
    latitude: float
    longitude: float
    emergency_type: str  # 'Trapped', 'Medical', 'Food/Water', 'Rescue Needed'
    notes: Optional[str] = None

class SOSAlertResponse(BaseModel):
    alert_id: str
    user_id: str
    user_name: str
    user_phone: str
    latitude: float
    longitude: float
    emergency_type: str
    status: str  # 'Pending', 'Dispatched', 'Rescued', 'Resolved'
    created_at: str
    notes: Optional[str] = None

class AlertBroadcastRequest(BaseModel):
    title: str
    body: str
    severity: str  # 'LOW', 'MODERATE', 'HIGH', 'CRITICAL'
    disaster_type: str  # 'FLOOD', 'LANDSLIDE', etc.
    target_region: str
    action_required: str
    send_push_notification: Optional[bool] = True
    trigger_emergency_siren: Optional[bool] = False

class AlertBroadcastResponse(BaseModel):
    alert_id: str
    title: str
    body: str
    severity: str
    disaster_type: str
    target_region: str
    issued_by: str
    issued_at: str
    action_required: str
    affected_population_estimate: Optional[int] = 42500
    acknowledgment_required: Optional[bool] = False

