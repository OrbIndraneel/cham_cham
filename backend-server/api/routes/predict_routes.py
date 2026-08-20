from fastapi import APIRouter, Depends
from api.schemas.disaster import HazardPredictionRequest, HazardPredictionResponse
from database.connection import get_db
from database.repositories import SpatialHazardRepository
from ml_engine.inference import CascadePredictor

router = APIRouter()
predictor = CascadePredictor()

@router.post("/predict-cascade", response_model=HazardPredictionResponse)
def predict_cascade(request: HazardPredictionRequest, db=Depends(get_db)):
    # Run PyTorch GAT ML Cascade Inference Engine
    res = predictor.predict_cascade_hazard(
        latitude=request.latitude,
        longitude=request.longitude,
        rainfall_mm=request.rainfall_mm,
        river_level_m=request.river_level_m,
        district_id=request.district_id
    )
    
    # Store hazard polygon in spatial DB if PostGIS connected
    repo = SpatialHazardRepository(db_session=db)
    repo.check_user_in_hazard_zone(request.latitude, request.longitude, [res["polygon_coordinates"]])
    
    return HazardPredictionResponse(
        district_id=res["district_id"],
        primary_hazard=res["primary_hazard"],
        secondary_cascade_hazard=res["secondary_cascade_hazard"],
        cascade_probability=res["cascade_probability"],
        estimated_lead_time_mins=res["estimated_lead_time_mins"],
        risk_level=res["risk_level"],
        affected_population_estimate=res["affected_population_estimate"],
        severity_score=res["severity_score"],
        soil_saturation_index=res["soil_saturation_index"],
        polygon_coordinates=res["polygon_coordinates"]
    )
