from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from api.schemas.disaster import SOSAlertRequest, SOSAlertResponse
from database.connection import get_db
from database.repositories import SpatialSOSRepository

router = APIRouter()

@router.post("/sos", response_model=SOSAlertResponse)
def create_emergency_sos_alert(request: SOSAlertRequest, db=Depends(get_db)):
    repo = SpatialSOSRepository(db_session=db)
    alert = repo.create_sos_alert(
        user_id=request.user_id,
        user_name=request.user_name,
        user_phone=request.user_phone,
        lat=request.latitude,
        lng=request.longitude,
        emergency_type=request.emergency_type,
        notes=request.notes
    )
    return alert

@router.get("/sos/active", response_model=List[SOSAlertResponse])
def get_active_sos_alerts(
    lat: Optional[float] = Query(31.1048, description="Center latitude"),
    lng: Optional[float] = Query(77.1734, description="Center longitude"),
    radius_km: Optional[float] = Query(50.0, description="Radius in km"),
    db=Depends(get_db)
):
    repo = SpatialSOSRepository(db_session=db)
    alerts = repo.get_active_sos_alerts(lat=lat, lng=lng, radius_km=radius_km)
    return alerts
