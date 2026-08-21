from risk_engine import compute_risk_level
from resource_engine import get_emergency_resources

# Add as many scenarios as you want to test here
test_scenarios = {
    "Low Risk": {
        "zone": {
            "Rainfall_mm": 40, "Temperature_C": 30, "Humidity_pct": 40,
            "River_Discharge_m3s": 60, "Water_Level_m": 0.8, "Elevation_m": 600,
            "Land_Cover": "Forest", "Soil_Type": "Sandy",
            "Population_Density": 100, "Infrastructure": 1, "Historical_Floods": 0
        },
        "lat": 22.310, "lon": 73.180
    },
    "Moderate Risk": {
        "zone": {
            "Rainfall_mm": 180, "Temperature_C": 28, "Humidity_pct": 65,
            "River_Discharge_m3s": 250, "Water_Level_m": 2.5, "Elevation_m": 250,
            "Land_Cover": "Agricultural", "Soil_Type": "Loam",
            "Population_Density": 500, "Infrastructure": 1, "Historical_Floods": 0
        },
        "lat": 22.310, "lon": 73.180
    },
    "Critical Risk": {
        "zone": {
            "Rainfall_mm": 650, "Temperature_C": 29, "Humidity_pct": 90,
            "River_Discharge_m3s": 900, "Water_Level_m": 8.5, "Elevation_m": 20,
            "Land_Cover": "Urban", "Soil_Type": "Clay",
            "Population_Density": 1500, "Infrastructure": 0, "Historical_Floods": 1
        },
        "lat": 22.310, "lon": 73.180
    },
}

for name, data in test_scenarios.items():
    print(f"\n{'='*50}")
    print(name)
    print('='*50)

    risk = compute_risk_level(data["zone"])
    print(f"Flood Probability: {risk['flood_probability']}")
    print(f"Risk Score       : {risk['risk_score']}")
    print(f"Risk Level       : {risk['risk_level']}")

    if risk["risk_level"] in ("Moderate", "High", "Critical"):
        resources = get_emergency_resources(data["lat"], data["lon"])
        print(f"Ambulance        : {resources['recommended_ambulance']}")
        print(f"Hospital         : {resources['recommended_hospital']}")
    else:
        print("No emergency resources needed (Low risk)")
