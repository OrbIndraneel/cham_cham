from fastapi import APIRouter
from api.schemas.disaster import EvacuationRouteRequest, EvacuationRouteResponse

router = APIRouter()

@router.post("/evacuation-route", response_model=EvacuationRouteResponse)
def calculate_evacuation_route(request: EvacuationRouteRequest):
    # TODO: Connect to Optimization Engine (OR-Tools)
    return EvacuationRouteResponse(
        route_id="route_opt_101",
        distance_km=4.2,
        estimated_time_mins=12,
        hazard_avoided=True,
        route_coordinates=[
            [request.user_lat, request.user_lng],
            [request.user_lat + 0.005, request.user_lng + 0.005],
            [request.user_lat + 0.010, request.user_lng + 0.012]
        ]
    )
