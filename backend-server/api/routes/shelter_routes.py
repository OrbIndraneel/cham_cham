from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from database.connection import get_db
from database.repositories import SpatialShelterRepository

router = APIRouter()

@router.get("/shelters")
def get_nearby_shelters(
    lat: float = Query(..., description="Latitude of user location"),
    lng: float = Query(..., description="Longitude of user location"),
    radius_km: Optional[float] = Query(15.0, description="Search radius in kilometers"),
    db=Depends(get_db)
):
    repo = SpatialShelterRepository(db_session=db)
    shelters = repo.get_nearby_shelters(lat=lat, lng=lng, radius_km=radius_km)
    return shelters
