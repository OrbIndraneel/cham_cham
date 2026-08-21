"""
[TEST RUN EXECUTION SCRIPT]
Runs real-time inference across diverse historical disaster scenarios using the trained GAT model.
"""
import os
import json
from ml_engine.inference import CascadePredictor

def run_test_simulation():
    predictor = CascadePredictor()

    test_scenarios = [
        {
            "name": "2024 Wayanad Saturation Landslide",
            "lat": 11.55,
            "lng": 76.15,
            "rain": 420.0,
            "river": 9.5,
            "slope": 44.0,
            "elevation": 1100.0,
            "district": "WAYANAD_01"
        },
        {
            "name": "2020 Sundarbans Amphan Cyclone",
            "lat": 21.80,
            "lng": 88.90,
            "rain": 310.0,
            "river": 6.2,
            "slope": 2.0,
            "elevation": 5.0,
            "district": "SUNDARBANS_01"
        },
        {
            "name": "2023 Kedarnath Mandakini Basin Flood",
            "lat": 30.73,
            "lng": 79.06,
            "rain": 380.0,
            "river": 14.5,
            "slope": 46.0,
            "elevation": 3500.0,
            "district": "CHAMOLI_01"
        },
        {
            "name": "2005 Mumbai Urban Coastal Deluge",
            "lat": 19.07,
            "lng": 72.87,
            "rain": 944.0,
            "river": 8.5,
            "slope": 6.0,
            "elevation": 12.0,
            "district": "MUMBAI_01"
        },
        {
            "name": "2025 Central-West Vadodara Flood",
            "lat": 22.30,
            "lng": 73.18,
            "rain": 280.0,
            "river": 7.8,
            "slope": 4.0,
            "elevation": 35.0,
            "district": "VADODARA_01"
        },
        {
            "name": "Deccan Plateau Dry Baseline",
            "lat": 17.38,
            "lng": 78.48,
            "rain": 5.0,
            "river": 0.8,
            "slope": 8.0,
            "elevation": 540.0,
            "district": "HYDERABAD_01"
        }
    ]

    print("=" * 80)
    print("             REAL-TIME GAT MODEL END-TO-END TEST RUN")
    print("=" * 80)

    for loc in test_scenarios:
        res = predictor.predict_cascade_hazard(
            latitude=loc["lat"],
            longitude=loc["lng"],
            rainfall_mm=loc["rain"],
            river_level_m=loc["river"],
            district_id=loc["district"],
            slope_angle_deg=loc["slope"],
            elevation_m=loc["elevation"]
        )
        print(f"\n[Target Scenario: {loc['name']}]")
        print(f"   Coordinates  : ({loc['lat']} N, {loc['lng']} E) | Elevation: {loc['elevation']}m | Slope: {loc['slope']} deg")
        print(f"   Inputs       : Rain={loc['rain']} mm | River Stage={loc['river']} m")
        print(f"   Predictions  : Cascade Prob={res['cascade_probability']} | Lead Time={res['estimated_lead_time_mins']} mins | Risk Level={res['risk_level']}")
        print(f"   Cascade Type : Primary={res['primary_hazard']} | Secondary={res['secondary_cascade_hazard']}")
        print(f"   Risk Polygon : Bounds NW {res['polygon_coordinates'][0]} to SE {res['polygon_coordinates'][2]}")
        print("-" * 80)

    print("\n[OK] Test Run Completed Successfully!")

if __name__ == "__main__":
    run_test_simulation()
