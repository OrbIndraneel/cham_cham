def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "Disaster Management AI Backend" in data["message"]

def test_get_shelters_endpoint(client):
    response = client.get("/api/shelters?lat=31.1048&lng=77.1734&radius_km=15")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    first_shelter = data[0]
    assert "shelter_id" in first_shelter
    assert "distance_km" in first_shelter
    assert first_shelter["status"] == "Open"
    assert "medical_facilities_available" in first_shelter

def test_predict_cascade_high_risk(client):
    payload = {
        "latitude": 31.1048,
        "longitude": 77.1734,
        "rainfall_mm": 125.0,
        "river_level_m": 8.5,
        "district_id": "DIST_SHIMLA_01"
    }
    response = client.post("/api/predict-cascade", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["district_id"] == "DIST_SHIMLA_01"
    assert data["risk_level"] == "High"
    assert data["cascade_probability"] >= 0.70
    assert len(data["polygon_coordinates"]) == 4

def test_predict_cascade_low_risk(client):
    payload = {
        "latitude": 31.1048,
        "longitude": 77.1734,
        "rainfall_mm": 15.0,
        "river_level_m": 2.1,
        "district_id": "DIST_SHIMLA_01"
    }
    response = client.post("/api/predict-cascade", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] == "Low"
    assert data["cascade_probability"] < 0.30

def test_evacuation_route_endpoint(client):
    payload = {
        "user_lat": 31.1048,
        "user_lng": 77.1734
    }
    response = client.post("/api/evacuation-route", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "route_id" in data
    assert data["hazard_avoided"] is True
    assert len(data["route_coordinates"]) >= 2
    assert data["distance_km"] > 0

def test_create_sos_alert_endpoint(client):
    payload = {
        "user_id": "user_shimla_99",
        "user_name": "Rohan Verma",
        "user_phone": "+91-98765-43210",
        "latitude": 31.1048,
        "longitude": 77.1734,
        "emergency_type": "Trapped",
        "notes": "Trapped near Mall Road due to debris flow."
    }
    response = client.post("/api/sos", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "alert_id" in data
    assert data["user_id"] == "user_shimla_99"
    assert data["status"] == "Pending"
    assert data["emergency_type"] == "Trapped"

def test_get_active_sos_alerts_endpoint(client):
    response = client.get("/api/sos/active?lat=31.1048&lng=77.1734&radius_km=50")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
