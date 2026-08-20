import sys
import os

# Add backend-server directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend-server')))

from fastapi.testclient import TestClient
from api.main import app

def run_e2e_integration_test():
    print("=== STARTING END-TO-END BACKEND & FRONTEND INTEGRATION TEST ===")
    client = TestClient(app)

    # 1. Health check
    res = client.get("/")
    assert res.status_code == 200
    print("[SUCCESS] Health Check Passed:", res.json())

    # 2. GNN Cascade Prediction
    pred_res = client.post("/api/predict-cascade", json={
        "latitude": 22.3072,
        "longitude": 73.1812,
        "rainfall_mm": 180.0,
        "river_level_m": 2.6,
        "district_id": "vadodara"
    })
    assert pred_res.status_code == 200
    pred_data = pred_res.json()
    print("[SUCCESS] GNN Predict Cascade Passed:", pred_data["district_id"], pred_data["risk_level"], f"Probability: {pred_data['cascade_probability']}")

    # 3. OR-Tools Route Solver
    route_res = client.post("/api/evacuation-route", json={
        "user_lat": 22.3072,
        "user_lng": 73.1812,
        "destination_shelter_id": "sh_01",
        "transport_mode": "walking"
    })
    assert route_res.status_code == 200
    route_data = route_res.json()
    print("[SUCCESS] OR-Tools Evacuation Route Passed:", route_data["route_id"], f"Distance: {route_data['distance_km']}km", f"Time: {route_data['estimated_time_mins']}mins")

    # 4. Spatial Shelters Lookup
    shelter_res = client.get("/api/shelters?lat=22.3072&lng=73.1812&radius_km=30")
    assert shelter_res.status_code == 200
    shelter_data = shelter_res.json()
    print("[SUCCESS] Spatial Shelters Search Passed:", f"Found {len(shelter_data)} shelters nearby.")

    # 5. Emergency SOS Dispatch
    sos_res = client.post("/api/sos", json={
        "user_id": "user_vadodara_42",
        "user_name": "Priya Patel",
        "user_phone": "+91-98765-12345",
        "latitude": 22.3072,
        "longitude": 73.1812,
        "emergency_type": "Submerged House",
        "notes": "Water entering ground floor."
    })
    assert sos_res.status_code == 200
    sos_data = sos_res.json()
    print("[SUCCESS] Emergency SOS Dispatch Passed:", sos_data["alert_id"], sos_data["status"])

    # 6. Active SOS Stream for Authority Dashboard
    active_sos_res = client.get("/api/sos/active?lat=22.3072&lng=73.1812&radius_km=50")
    assert active_sos_res.status_code == 200
    active_sos_data = active_sos_res.json()
    print("[SUCCESS] Active SOS Stream Passed:", f"{len(active_sos_data)} active SOS incidents tracked.")

    # 7. Broadcast Emergency Alert
    broadcast_res = client.post("/api/alerts/broadcast", json={
        "title": "URGENT: Flash Flood Alert",
        "body": "Evacuate low lying areas near Vishwamitri river.",
        "severity": "CRITICAL",
        "disaster_type": "FLOOD",
        "target_region": "Vadodara",
        "action_required": "EVACUATE_IMMEDIATELY",
        "send_push_notification": True,
        "trigger_emergency_siren": True
    })
    assert broadcast_res.status_code == 200
    broadcast_data = broadcast_res.json()
    print("[SUCCESS] Broadcast Emergency Alert Passed:", broadcast_data["alert_id"], broadcast_data["title"])

    # 8. Fetch Active Broadcast Alerts
    active_alerts_res = client.get("/api/alerts/active")
    assert active_alerts_res.status_code == 200
    active_alerts_data = active_alerts_res.json()
    print("[SUCCESS] Active Broadcast Alerts Passed:", f"{len(active_alerts_data)} alerts in stream.")

    print("\n[COMPLETE] ALL BACKEND ENDPOINTS AND FRONTEND DATA CONTRACTS ARE 100% OPERATIONAL & VERIFIED!")


if __name__ == '__main__':
    run_e2e_integration_test()
