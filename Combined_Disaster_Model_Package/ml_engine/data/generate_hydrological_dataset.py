"""
[HYDROLOGICAL SYNTHETIC DATASET GENERATOR (2000-2026 BENCHMARK)]
Generates large-scale, physically-grounded synthetic hydrological datasets derived from 
IMD and CWC benchmark metrics (2000-2026 extreme events).

Includes GEV peak 24h rainfall distribution, Log-Normal monthly departure, river stage elevation 
thresholds, IMD severity classification, and spatial graph builder integration for GAT models.
"""
import os
import math
import json
import random
import numpy as np
import pandas as pd
from scipy.stats import genextreme, lognorm

# Set seed for reproducible benchmark dataset generation
np.random.seed(42)
random.seed(42)

# -----------------------------------------------------------------------------
# 1. Historical Benchmark River Basin Profiles (IMD & CWC Station Data)
# -----------------------------------------------------------------------------
RIVER_BASIN_PROFILES = [
    {
        "basin": "Yamuna River Basin",
        "station": "Old Railway Bridge (Delhi)",
        "danger_level_m": 205.33,
        "peak_level_m": 208.66,
        "base_elevation_m": 210.0,
        "base_slope_deg": 18.0,
        "region_type": "Urban/Riverine Plains"
    },
    {
        "basin": "Brahmaputra Valley",
        "station": "Guwahati (Nehru Park, Assam)",
        "danger_level_m": 49.68,
        "peak_level_m": 51.46,
        "base_elevation_m": 55.0,
        "base_slope_deg": 28.0,
        "region_type": "NE Catchment/Valley"
    },
    {
        "basin": "Ganga Basin",
        "station": "Bhagalpur (Bihar)",
        "danger_level_m": 31.09,
        "peak_level_m": 34.17,
        "base_elevation_m": 40.0,
        "base_slope_deg": 15.0,
        "region_type": "Floodplain Siltation Belt"
    },
    {
        "basin": "Jhelum River Basin",
        "station": "Sangam (Anantnag, J&K)",
        "danger_level_m": 6.40,
        "peak_level_m": 10.05,
        "base_elevation_m": 1600.0,
        "base_slope_deg": 35.0,
        "region_type": "High Altitude Valley"
    },
    {
        "basin": "Mahanadi Basin",
        "station": "Mundali (Odisha)",
        "danger_level_m": 29.57,
        "peak_level_m": 33.10,
        "base_elevation_m": 35.0,
        "base_slope_deg": 20.0,
        "region_type": "Deltaic Catchment"
    },
    {
        "basin": "Konkan & Western Ghats",
        "station": "Mahad / Chiplun / Mumbai",
        "danger_level_m": 7.00,
        "peak_level_m": 12.50,
        "base_elevation_m": 450.0,
        "base_slope_deg": 42.0,
        "region_type": "Coastal-Ghat Escarpment"
    },
    {
        "basin": "Upper Himalayan Catchment",
        "station": "Manali / Mandi / Kedarnath",
        "danger_level_m": 12.00,
        "peak_level_m": 18.50,
        "base_elevation_m": 2400.0,
        "base_slope_deg": 45.0,
        "region_type": "Alpine Mountain Trough"
    }
]

def classify_imd_severity(mm: float) -> str:
    """Classifies rainfall according to IMD quantitative precipitation benchmarks."""
    if mm < 115.5:
        return "Heavy"
    elif mm < 204.4:
        return "Very Heavy"
    elif mm < 400.0:
        return "Extremely Heavy"
    else:
        return "Cloudburst / Catastrophic"

def determine_intensity_regime(hourly_peak_mm: float) -> str:
    """Categorizes peak hourly intensity into meteorological regimes."""
    if hourly_peak_mm < 40.0:
        return "Normal Monsoon Regime"
    elif hourly_peak_mm <= 80.0:
        return "Urban Inundation Threshold"
    else:
        return "Cloudburst Flash Flood Regime"

def generate_hydrological_dataset(n_samples: int = 10000, output_dir: str = None) -> pd.DataFrame:
    """
    Generates synthetic benchmark dataset of n_samples extreme precipitation events (2000-2026).
    Uses GEV for daily peak precipitation, Log-Normal for monthly anomalies, and 
    physically-motivated river stage calculations.
    """
    print(f"Generating {n_samples:,} synthetic hydrological event records...")

    # 1. GEV Distribution Parameters (Location=215.4, Scale=84.2, Shape=0.38)
    # Scipy genextreme uses shape parameter c = -xi
    shape_xi = -0.38
    loc_mu = 215.4
    scale_sigma = 84.2

    # Draw 24-hour peak precipitation depth (mm)
    raw_p24 = genextreme.rvs(c=shape_xi, loc=loc_mu, scale=scale_sigma, size=n_samples)
    p24_mm = np.clip(raw_p24, 80.0, 1000.0)

    # 2. Log-Normal Monthly Precipitation Departure (% Deviation)
    # Mean log mu=4.82, sigma=0.54
    lognorm_mu = 4.82
    lognorm_sigma = 0.54
    # lognorm in scipy takes s=sigma, scale=exp(mu)
    departure_pct = np.random.lognormal(mean=lognorm_mu, sigma=lognorm_sigma, size=n_samples)
    departure_pct = np.clip(departure_pct, 10.0, 1500.0)

    # 3. Peak Hourly Rainfall Intensity (mm/hr)
    # Cloudburst vs Non-Cloudburst behavior
    intensity_ratio = np.random.uniform(0.18, 0.35, n_samples)
    # Add intensity spike for cloudburst regime (> 400mm 24h rain)
    cloudburst_mask = (p24_mm >= 400.0)
    intensity_ratio[cloudburst_mask] = np.random.uniform(0.35, 0.55, np.sum(cloudburst_mask))
    hourly_peak_mm = p24_mm * intensity_ratio

    # Build dataset records
    records = []
    for i in range(n_samples):
        # Sample event metadata
        event_id = i + 1
        year = random.randint(2000, 2026)
        basin_info = random.choice(RIVER_BASIN_PROFILES)
        
        rain = round(float(p24_mm[i]), 2)
        dep = round(float(departure_pct[i]), 2)
        peak_hr = round(float(hourly_peak_mm[i]), 2)
        
        # Calculate river water level based on danger mark, rainfall, and departure anomaly
        danger_m = basin_info["danger_level_m"]
        peak_historical_m = basin_info["peak_level_m"]
        
        # River level surge relative to rain and departure
        surge_factor = min(1.3, (rain / 300.0) * (0.8 + 0.4 * (dep / 200.0)))
        river_level_m = danger_m - 1.5 + surge_factor * (peak_historical_m - danger_m + 2.0)
        river_level_m = round(max(0.5, river_level_m + random.uniform(-0.4, 0.4)), 2)
        
        danger_departure_m = round(river_level_m - danger_m, 2)
        
        # Soil saturation index (0.0 - 1.0)
        soil_sat = min(1.0, max(0.2, (rain / 250.0) * 0.6 + (dep / 300.0) * 0.4))
        soil_sat = round(soil_sat, 3)

        # Vegetation NDVI & Slope
        slope_deg = round(basin_info["base_slope_deg"] + random.uniform(-4.0, 4.0), 1)
        elevation_m = round(basin_info["base_elevation_m"] + random.uniform(-100, 100), 1)
        ndvi = round(max(0.15, min(0.85, 0.50 + random.uniform(-0.25, 0.25))), 2)

        # Classification
        imd_category = classify_imd_severity(rain)
        intensity_regime = determine_intensity_regime(peak_hr)

        # Ground-truth GNN / ML Target Generation:
        # Cascade probability z score
        z = (rain - 180.0) / 45.0 + (river_level_m - danger_m) / 1.2 + (soil_sat - 0.7) / 0.15 + (slope_deg - 30.0) / 12.0
        prob_target = 1.0 / (1.0 + math.exp(-z))
        # Add slight observational noise
        prob_target = float(np.clip(prob_target + np.random.normal(0, 0.03), 0.01, 0.99))
        prob_target = round(prob_target, 4)

        # Lead time target (mins)
        lead_time_target = float(np.clip(120.0 - (prob_target * 85.0) + random.uniform(-5.0, 5.0), 15.0, 180.0))
        lead_time_target = round(lead_time_target, 1)

        # Risk level classification
        if prob_target >= 0.70:
            risk_level = "High"
            secondary_hazard = "Landslide & Flash Flood" if slope_deg > 30.0 else "Urban Inundation"
        elif prob_target >= 0.35:
            risk_level = "Medium"
            secondary_hazard = "Debris Flow" if slope_deg > 25.0 else "River Swell"
        else:
            risk_level = "Low"
            secondary_hazard = "None"

        records.append({
            "Synthetic_Event_ID": event_id,
            "Year": year,
            "River_Basin": basin_info["basin"],
            "Gauging_Station": basin_info["station"],
            "Region_Type": basin_info["region_type"],
            "Peak_24h_Rainfall_mm": rain,
            "Monthly_Monsoon_Departure_Pct": dep,
            "Peak_Hourly_Intensity_mm_hr": peak_hr,
            "Intensity_Regime": intensity_regime,
            "River_Level_m": river_level_m,
            "River_Danger_Level_m": danger_m,
            "River_Danger_Departure_m": danger_departure_m,
            "Soil_Saturation_Index": soil_sat,
            "Terrain_Slope_Deg": slope_deg,
            "Elevation_m": elevation_m,
            "Vegetation_NDVI": ndvi,
            "IMD_Severity_Category": imd_category,
            "Cascade_Probability": prob_target,
            "Estimated_Lead_Time_Mins": lead_time_target,
            "Risk_Level": risk_level,
            "Secondary_Cascade_Hazard": secondary_hazard
        })

    df = pd.DataFrame(records)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        csv_path = os.path.join(output_dir, "hydrological_synthetic_dataset_2000_2026.csv")
        json_path = os.path.join(output_dir, "hydrological_synthetic_dataset_2000_2026.json")
        
        df.to_csv(csv_path, index=False)
        df.to_json(json_path, orient="records", indent=2)
        print(f"[OK] Successfully saved dataset ({len(df):,} rows):")
        print(f"   - CSV:  {csv_path}")
        print(f"   - JSON: {json_path}")

    return df

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "datasets")
    df = generate_hydrological_dataset(n_samples=10000, output_dir=output_dir)
    print("\nDataset Summary Statistics:")
    print(df[["Peak_24h_Rainfall_mm", "Monthly_Monsoon_Departure_Pct", "Peak_Hourly_Intensity_mm_hr", "River_Level_m", "Cascade_Probability", "Estimated_Lead_Time_Mins"]].describe())
    print("\nSample Data (First 5 Rows):")
    print(df.head(5))
