from fastapi import APIRouter, Depends
from api.schemas.disaster import HazardPredictionRequest, HazardPredictionResponse
from database.connection import get_db
from database.repositories import SpatialHazardRepository

router = APIRouter()

@router.post("/predict-cascade", response_model=HazardPredictionResponse)
def predict_cascade(request: HazardPredictionRequest, db=Depends(get_db)):
    # Calculate hazard risk dynamically based on precipitation & hydrological data
    rainfall = request.rainfall_mm
    river = request.river_level_m or 0.0
    
    if rainfall >= 100.0 or river >= 8.0:
        cascade_prob = min(0.95, 0.70 + (rainfall / 500.0))
        primary = "Heavy Rainfall"
        secondary = "Landslide & Flash Flood"
        risk_lvl = "High"
        lead_time = 35
    elif rainfall >= 50.0:
        cascade_prob = 0.60
        primary = "Moderate Rainfall"
        secondary = "Debris Flow"
        risk_lvl = "Medium"
        lead_time = 90
    else:
        cascade_prob = 0.15
        primary = "Light Rainfall"
        secondary = "None"
        risk_lvl = "Low"
        lead_time = 240

    # Risk polygon surrounding the request coordinates
    lat, lng = request.latitude, request.longitude
    offset = 0.015 if risk_lvl == "High" else 0.008
    polygon_coords = [
        [lat + offset, lng - offset],
        [lat + offset, lng + offset],
        [lat - offset, lng + offset],
        [lat - offset, lng - offset]
    ]

    repo = SpatialHazardRepository(db_session=db)
    is_in_risk_zone = repo.check_user_in_hazard_zone(lat, lng, [polygon_coords])

    return HazardPredictionResponse(
        district_id=request.district_id,
        primary_hazard=primary,
        secondary_cascade_hazard=secondary,
        cascade_probability=round(cascade_prob, 2),
        estimated_lead_time_mins=lead_time,
        risk_level=risk_lvl,
        polygon_coordinates=polygon_coords
    )
