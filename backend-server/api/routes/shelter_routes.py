from fastapi import APIRouter

router = APIRouter()

@router.get("/shelters")
def get_nearby_shelters(lat: float, lng: float):
    return [
        {
            "shelter_id": "sh_01",
            "name": "Government Senior School Relief Camp",
            "latitude": lat + 0.010,
            "longitude": lng + 0.012,
            "capacity": 500,
            "current_occupancy": 120,
            "status": "Open"
        },
        {
            "shelter_id": "sh_02",
            "name": "Community Hall Emergency Shelter",
            "latitude": lat - 0.008,
            "longitude": lng - 0.005,
            "capacity": 300,
            "current_occupancy": 45,
            "status": "Open"
        }
    ]
