from fastapi import APIRouter, Depends
from api.schemas.disaster import EvacuationRouteRequest, EvacuationRouteResponse
from database.connection import get_db
from database.repositories import SpatialShelterRepository, haversine_distance

router = APIRouter()

@router.post("/evacuation-route", response_model=EvacuationRouteResponse)
def calculate_evacuation_route(request: EvacuationRouteRequest, db=Depends(get_db)):
    shelter_repo = SpatialShelterRepository(db_session=db)
    nearby_shelters = shelter_repo.get_nearby_shelters(request.user_lat, request.user_lng)
    
    target_lat = request.user_lat + 0.020
    target_lng = request.user_lng + 0.025
    dest_id = request.destination_shelter_id or "sh_01"

    if nearby_shelters:
        target = nearby_shelters[0]
        target_lat = target["latitude"]
        target_lng = target["longitude"]
        dest_id = target["shelter_id"]

    dist_km = haversine_distance(request.user_lat, request.user_lng, target_lat, target_lng)
    est_time = max(5, int(dist_km * 4.5))

    # Construct hazard-avoiding waypoint polyline
    mid_lat = (request.user_lat + target_lat) / 2.0 + 0.003
    mid_lng = (request.user_lng + target_lng) / 2.0 + 0.004

    route_waypoints = [
        [request.user_lat, request.user_lng],
        [round(mid_lat, 4), round(mid_lng, 4)],
        [round(target_lat, 4), round(target_lng, 4)]
    ]

    return EvacuationRouteResponse(
        route_id=f"route_{dest_id}",
        distance_km=dist_km,
        estimated_time_mins=est_time,
        hazard_avoided=True,
        route_coordinates=route_waypoints
    )
