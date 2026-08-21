"""
Risk Engine — Person A's second deliverable
Takes the raw flood probability from the ML model and combines it with
population density, elevation, and historical vulnerability to produce
a final RISK LEVEL. This is the function Person B calls from the API.

This is deliberately a plain importable function (not wrapped in FastAPI)
so Person B can plug it straight into their decision engine.
"""

import pickle
import numpy as np
import pandas as pd
from xgboost import XGBClassifier

MODEL_PATH = "flood_model.json"
ENCODERS_PATH = "encoders.pkl"

_model = XGBClassifier()
_model.load_model(MODEL_PATH)

with open(ENCODERS_PATH, "rb") as f:
    _encoders = pickle.load(f)

FEATURE_COLS = [
    "Rainfall_mm", "Temperature_C", "Humidity_pct", "River_Discharge_m3s",
    "Water_Level_m", "Elevation_m", "Land_Cover", "Soil_Type",
    "Population_Density", "Infrastructure", "Historical_Floods",
]


def predict_flood_probability(zone_data: dict) -> float:
    """
    zone_data must contain all FEATURE_COLS as raw values, e.g.:
    {
        "Rainfall_mm": 320.5, "Temperature_C": 29.1, "Humidity_pct": 85,
        "River_Discharge_m3s": 610, "Water_Level_m": 4.2, "Elevation_m": 45,
        "Land_Cover": "Urban", "Soil_Type": "Clay",
        "Population_Density": 1200, "Infrastructure": 1, "Historical_Floods": 1
    }
    Returns flood probability (0-1 float).
    """
    row = zone_data.copy()
    for col, encoder in _encoders.items():
        row[col] = encoder.transform([row[col]])[0]

    X = pd.DataFrame([row])[FEATURE_COLS]
    proba = _model.predict_proba(X)[0][1]
    return float(proba)


def compute_risk_level(zone_data: dict) -> dict:
    """
    Combines model flood probability with population density, elevation,
    and historical vulnerability to produce a final risk assessment.

    Returns:
    {
        "flood_probability": 0.87,
        "risk_score": 0.81,
        "risk_level": "Critical",
        "factors": {...}   # breakdown, useful for demo/explainability
    }
    """
    flood_prob = predict_flood_probability(zone_data)

    population_density = zone_data["Population_Density"]
    elevation = zone_data["Elevation_m"]
    historical_floods = zone_data["Historical_Floods"]
    infrastructure = zone_data["Infrastructure"]

    # Normalize secondary factors (rough India-scale bounds)
    pop_factor = min(population_density / 2000, 1.0)          # dense urban ~2000+/km2
    elevation_factor = 1 - min(elevation / 500, 1.0)           # lower elevation = higher risk
    history_factor = 1.0 if historical_floods else 0.0
    infra_factor = 0.0 if infrastructure else 1.0               # no infra = higher risk

    # Weighted combination -> final risk score
    risk_score = (
        0.55 * flood_prob
        + 0.15 * pop_factor
        + 0.15 * elevation_factor
        + 0.10 * history_factor
        + 0.05 * infra_factor
    )
    risk_score = round(min(risk_score, 1.0), 3)

    if risk_score >= 0.75:
        level = "Critical"
    elif risk_score >= 0.55:
        level = "High"
    elif risk_score >= 0.30:
        level = "Moderate"
    else:
        level = "Low"

    return {
        "flood_probability": round(flood_prob, 3),
        "risk_score": risk_score,
        "risk_level": level,
        "factors": {
            "population_density_factor": round(pop_factor, 3),
            "elevation_factor": round(elevation_factor, 3),
            "historical_floods_factor": history_factor,
            "infrastructure_factor": infra_factor,
        },
    }


if __name__ == "__main__":
    # Quick manual test
    sample_zone = {
        "Rainfall_mm": 420.0,
        "Temperature_C": 29.5,
        "Humidity_pct": 88,
        "River_Discharge_m3s": 780,
        "Water_Level_m": 5.1,
        "Elevation_m": 30,
        "Land_Cover": "Urban",
        "Soil_Type": "Clay",
        "Population_Density": 1500,
        "Infrastructure": 0,
        "Historical_Floods": 1,
    }
    result = compute_risk_level(sample_zone)
    print("Sample zone risk assessment:")
    for k, v in result.items():
        print(f"  {k}: {v}")
