"""
Resource Engine — finds available ambulances and nearest hospitals for a
given location, and scores them (not just "nearest") so the recommendation
accounts for availability, capacity, and route status too.

Uses mock data (clearly labeled) — swap MOCK_AMBULANCES / MOCK_HOSPITALS
with real data later without changing any function signatures.
"""

import math

# ---------------------------------------------------------------
# Mock data — replace with real DB/API data later.
# lat/lon are sample coordinates around a generic Indian city center
# so distances are realistic. Swap with real hospital/ambulance data
# for your actual demo city.
# ---------------------------------------------------------------
MOCK_AMBULANCES = [
    {"id": "A01", "lat": 22.310, "lon": 73.181, "available": True,  "eta_min": 8,  "route_status": "Clear"},
    {"id": "A02", "lat": 22.305, "lon": 73.170, "available": False, "eta_min": None, "route_status": "Clear"},
    {"id": "A03", "lat": 22.320, "lon": 73.190, "available": True,  "eta_min": 6,  "route_status": "Clear"},
    {"id": "A04", "lat": 22.295, "lon": 73.160, "available": True,  "eta_min": 15, "route_status": "Blocked"},
    {"id": "A05", "lat": 22.330, "lon": 73.200, "available": True,  "eta_min": 12, "route_status": "Clear"},
]

MOCK_HOSPITALS = [
    {"id": "H01", "name": "City General Hospital", "lat": 22.315, "lon": 73.185, "beds_available": 34, "capacity_pct": 60, "route_status": "Clear"},
    {"id": "H02", "name": "Riverside Medical Center", "lat": 22.298, "lon": 73.165, "beds_available": 5,  "capacity_pct": 92, "route_status": "Clear"},
    {"id": "H03", "name": "St. Mary's Hospital", "lat": 22.325, "lon": 73.195, "beds_available": 18, "capacity_pct": 75, "route_status": "Blocked"},
    {"id": "H04", "name": "Government District Hospital", "lat": 22.290, "lon": 73.175, "beds_available": 40, "capacity_pct": 45, "route_status": "Clear"},
]


def haversine_distance_km(lat1, lon1, lat2, lon2):
    """Straight-line distance between two coordinates, in km."""
    R = 6371  # Earth radius km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return round(R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 2)


def find_best_ambulance(zone_lat, zone_lon):
    """
    Scores available ambulances by distance + ETA + route status.
    Returns the best one, or None if nothing is available.
    """
    candidates = []
    for amb in MOCK_AMBULANCES:
        if not amb["available"]:
            continue
        distance = haversine_distance_km(zone_lat, zone_lon, amb["lat"], amb["lon"])

        # Lower is better: normalize distance (0-15km) and eta (0-20min), penalize blocked routes
        distance_score = min(distance / 15, 1.0)
        eta_score = min(amb["eta_min"] / 20, 1.0)
        route_penalty = 0.3 if amb["route_status"] == "Blocked" else 0.0

        # Weighted cost (lower = better)
        cost = 0.45 * distance_score + 0.35 * eta_score + 0.20 * route_penalty

        candidates.append({**amb, "distance_km": distance, "cost": round(cost, 3)})

    if not candidates:
        return None

    candidates.sort(key=lambda c: c["cost"])
    best = candidates[0]
    return {
        "ambulance_id": best["id"],
        "distance_km": best["distance_km"],
        "eta_min": best["eta_min"],
        "route_status": best["route_status"],
    }


def find_best_hospital(zone_lat, zone_lon):
    """
    Scores hospitals by distance + bed availability + capacity + route status.
    Picks the best overall option, not just the nearest.
    """
    candidates = []
    for h in MOCK_HOSPITALS:
        distance = haversine_distance_km(zone_lat, zone_lon, h["lat"], h["lon"])

        distance_score = min(distance / 15, 1.0)          # lower better
        availability_score = 1 - min(h["beds_available"] / 40, 1.0)  # lower better (more beds = lower score)
        capacity_score = h["capacity_pct"] / 100            # lower better (less full = better, so this IS the "bad" score)
        route_penalty = 0.3 if h["route_status"] == "Blocked" else 0.0

        cost = (
            0.30 * distance_score
            + 0.25 * availability_score
            + 0.25 * capacity_score
            + 0.20 * route_penalty
        )

        candidates.append({**h, "distance_km": distance, "cost": round(cost, 3)})

    candidates.sort(key=lambda c: c["cost"])
    best = candidates[0]
    return {
        "hospital_id": best["id"],
        "hospital_name": best["name"],
        "distance_km": best["distance_km"],
        "beds_available": best["beds_available"],
        "capacity_pct": best["capacity_pct"],
        "route_status": best["route_status"],
    }


def get_emergency_resources(zone_lat, zone_lon):
    """
    Main function Person B's API calls. Given a location, returns the
    best ambulance and best hospital recommendation.
    """
    return {
        "recommended_ambulance": find_best_ambulance(zone_lat, zone_lon),
        "recommended_hospital": find_best_hospital(zone_lat, zone_lon),
    }


if __name__ == "__main__":
    # Quick manual test — coordinates near the mock data cluster
    result = get_emergency_resources(22.310, 73.180)
    import json
    print(json.dumps(result, indent=2))
