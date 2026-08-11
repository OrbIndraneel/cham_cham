from fastapi import APIRouter
from api.schemas.disaster import HazardPredictionRequest, HazardPredictionResponse

router = APIRouter()

@router.post("/predict-cascade", response_model=HazardPredictionResponse)
def predict_cascade(request: HazardPredictionRequest):
    # TODO: Connect to ML Engine GNN model inference
    return HazardPredictionResponse(
        district_id=request.district_id,
        primary_hazard="Heavy Rainfall",
        secondary_cascade_hazard="Landslide",
        cascade_probability=0.88,
        estimated_lead_time_mins=45,
        risk_level="High",
        polygon_coordinates=[[31.1048, 77.1734], [31.1100, 77.1800], [31.0950, 77.1900]]
    )
