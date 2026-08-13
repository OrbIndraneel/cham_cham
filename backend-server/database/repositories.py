"""
[SPATIAL REPOSITORY LAYER] Geospatial queries for shelters, hazard risk zones, evacuation routes, and SOS emergency alerts.
"""
import math
import uuid
import datetime
from typing import List, Dict, Any, Optional

# Mock sample shelter database for fallback execution
MOCK_SHELTERS: List[Dict[str, Any]] = [
    {
        "shelter_id": "sh_01",
        "name": "Government Senior Secondary School Relief Camp",
        "latitude": 31.1148,
        "longitude": 77.1854,
        "capacity": 500,
        "current_occupancy": 120,
        "status": "Open",
        "address": "Mall Road, Shimla, HP",
        "contact": "+91-177-2800101",
        "medical_facilities_available": True,
        "food_supplies_days": 7,
        "power_generator": True,
        "helipad_access": False,
        "water_supply_liters": 5000,
        "admin_incharge_name": "Dr. Rajesh Sharma",
        "admin_incharge_phone": "+91-98160-11111"
    },
    {
        "shelter_id": "sh_02",
        "name": "Community Hall Emergency Relief Center",
        "latitude": 31.0968,
        "longitude": 77.1684,
        "capacity": 300,
        "current_occupancy": 45,
        "status": "Open",
        "address": "Sanjauli Sector 2, Shimla, HP",
        "contact": "+91-177-2800102",
        "medical_facilities_available": True,
        "food_supplies_days": 5,
        "power_generator": True,
        "helipad_access": False,
        "water_supply_liters": 3000,
        "admin_incharge_name": "Smt. Sunita Verma",
        "admin_incharge_phone": "+91-98160-22222"
    },
    {
        "shelter_id": "sh_03",
        "name": "District Indoor Sports Complex",
        "latitude": 31.1200,
        "longitude": 77.1950,
        "capacity": 800,
        "current_occupancy": 310,
        "status": "Open",
        "address": "Kasumpti, Shimla, HP",
        "contact": "+91-177-2800103",
        "medical_facilities_available": True,
        "food_supplies_days": 10,
        "power_generator": True,
        "helipad_access": True,
        "water_supply_liters": 10000,
        "admin_incharge_name": "Major Vikram Singh",
        "admin_incharge_phone": "+91-98160-33333"
    }
]

MOCK_SOS_ALERTS: List[Dict[str, Any]] = []

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates distance between two coordinates in kilometers using Haversine formula."""
    R = 6371.0  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

def point_in_polygon(lat: float, lng: float, polygon: List[List[float]]) -> bool:
    """Ray-casting algorithm to test if a (lat, lng) point is inside a polygon."""
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if lat > min(p1x, p2x):
            if lat <= max(p1x, p2x):
                if lng <= max(p1y, p2y):
                    if p1x != p2x:
                        xinters = (lat - p1x) * (p2y - p1y) / (p2x - p1x) + p1y
                    if p1y == p2y or lng <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

class SpatialShelterRepository:
    def __init__(self, db_session=None):
        self.db = db_session

    def get_nearby_shelters(self, lat: float, lng: float, radius_km: float = 15.0) -> List[Dict[str, Any]]:
        """Finds all open shelters within radius, returning amenities and capacity."""
        if self.db is not None:
            try:
                from sqlalchemy import text
                query = text("""
                    SELECT id, name, capacity, current_occupancy, status, address, contact,
                           medical_facilities_available, food_supplies_days, power_generator,
                           helipad_access, water_supply_liters, admin_incharge_name, admin_incharge_phone,
                           ST_Y(location::geometry) as latitude,
                           ST_X(location::geometry) as longitude,
                           ST_DistanceSphere(location, ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)) / 1000.0 as distance_km
                    FROM shelters
                    WHERE status = 'Open'
                      AND ST_DWithin(location, ST_SetSRID(ST_MakePoint(:lng, :lat), 4326), :radius_m)
                    ORDER BY distance_km ASC;
                """)
                result = self.db.execute(query, {"lat": lat, "lng": lng, "radius_m": radius_km * 1000.0})
                shelter_list = []
                for row in result:
                    item = dict(row._mapping)
                    item["shelter_id"] = item["id"]
                    item["distance_km"] = round(float(item["distance_km"]), 2)
                    shelter_list.append(item)
                if shelter_list:
                    return shelter_list
            except Exception as e:
                print(f"Error in spatial shelter query: {e}")
                pass
        
        # Fallback using Haversine distance
        results = []
        for s in MOCK_SHELTERS:
            dist = haversine_distance(lat, lng, s["latitude"], s["longitude"])
            if dist <= radius_km:
                shelter_item = dict(s)
                shelter_item["distance_km"] = dist
                results.append(shelter_item)
        results.sort(key=lambda x: x["distance_km"])
        return results

class SpatialHazardRepository:
    def __init__(self, db_session=None):
        self.db = db_session

    def check_user_in_hazard_zone(self, lat: float, lng: float, active_polygons: List[List[List[float]]]) -> bool:
        """Evaluates whether user location falls within any active risk polygon."""
        if self.db is not None:
            try:
                from sqlalchemy import text
                query = text("""
                    SELECT id FROM hazard_zones
                    WHERE is_active = TRUE
                      AND ST_Contains(geometry, ST_SetSRID(ST_MakePoint(:lng, :lat), 4326));
                """)
                res = self.db.execute(query, {"lat": lat, "lng": lng}).fetchall()
                if len(res) > 0:
                    return True
            except Exception:
                pass

        # Fallback ray-casting spatial check
        for polygon in active_polygons:
            if point_in_polygon(lat, lng, polygon):
                return True
        return False

class SpatialSOSRepository:
    def __init__(self, db_session=None):
        self.db = db_session

    def create_sos_alert(self, user_id: str, user_name: str, user_phone: str, lat: float, lng: float, emergency_type: str, notes: Optional[str] = None) -> Dict[str, Any]:
        """Creates a high-priority emergency rescue SOS alert in PostGIS."""
        alert_id = str(uuid.uuid4())
        created_at_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        if self.db is not None:
            try:
                from sqlalchemy import text
                query = text("""
                    INSERT INTO sos_alerts (id, user_id, user_name, user_phone, location, emergency_type, status, notes)
                    VALUES (:id, :user_id, :user_name, :user_phone, ST_SetSRID(ST_MakePoint(:lng, :lat), 4326), :emergency_type, 'Pending', :notes)
                    RETURNING id, user_id, user_name, user_phone, emergency_type, status, notes, created_at;
                """)
                res = self.db.execute(query, {
                    "id": alert_id,
                    "user_id": user_id,
                    "user_name": user_name,
                    "user_phone": user_phone,
                    "lat": lat,
                    "lng": lng,
                    "emergency_type": emergency_type,
                    "notes": notes
                }).fetchone()
                self.db.commit()
                if res:
                    row_dict = dict(res._mapping)
                    return {
                        "alert_id": str(row_dict["id"]),
                        "user_id": row_dict["user_id"],
                        "user_name": row_dict["user_name"],
                        "user_phone": row_dict["user_phone"],
                        "latitude": lat,
                        "longitude": lng,
                        "emergency_type": row_dict["emergency_type"],
                        "status": row_dict["status"],
                        "created_at": str(row_dict["created_at"]),
                        "notes": row_dict["notes"]
                    }
            except Exception as e:
                print(f"Error saving SOS alert: {e}")
                pass

        # Fallback in-memory list
        item = {
            "alert_id": alert_id,
            "user_id": user_id,
            "user_name": user_name or "Anonymous",
            "user_phone": user_phone or "N/A",
            "latitude": lat,
            "longitude": lng,
            "emergency_type": emergency_type,
            "status": "Pending",
            "created_at": created_at_str,
            "notes": notes
        }
        MOCK_SOS_ALERTS.append(item)
        return item

    def get_active_sos_alerts(self, lat: float = 31.1048, lng: float = 77.1734, radius_km: float = 50.0) -> List[Dict[str, Any]]:
        """Finds all active emergency rescue requests."""
        if self.db is not None:
            try:
                from sqlalchemy import text
                query = text("""
                    SELECT id, user_id, user_name, user_phone, emergency_type, status, notes, created_at,
                           ST_Y(location::geometry) as latitude,
                           ST_X(location::geometry) as longitude
                    FROM sos_alerts
                    WHERE status IN ('Pending', 'Dispatched')
                    ORDER BY created_at DESC;
                """)
                result = self.db.execute(query).fetchall()
                alerts = []
                for r in result:
                    item = dict(r._mapping)
                    item["alert_id"] = str(item["id"])
                    item["created_at"] = str(item["created_at"])
                    alerts.append(item)
                if alerts:
                    return alerts
            except Exception as e:
                print(f"Error querying active SOS alerts: {e}")
                pass

        return [a for a in MOCK_SOS_ALERTS if a["status"] in ("Pending", "Dispatched")]
