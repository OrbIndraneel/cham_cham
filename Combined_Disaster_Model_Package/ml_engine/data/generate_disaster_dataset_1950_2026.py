"""
[DISASTER SYNTHETIC DATASET GENERATOR (1950-2026 BENCHMARK)]
Generates 30,000 physically-grounded synthetic disaster event records derived from 
India_Natural_Disasters_Report_1950_2026 historical benchmarks.

Covers 76 years of multi-hazard events: Earthquakes, Super Cyclones, Riverine & Urban Floods,
Cloudbursts & GLOFs, Pan-Indian Droughts, Landslides, Avalanches, and Subsidence.
Includes non-stationary decadal shifts, ENSO/ONI coupling, SST anomalies, and strict boundary rules.
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
# 1. Historical Benchmark Event Profiles (1950-2026 Report Grounding)
# -----------------------------------------------------------------------------
HISTORICAL_BENCHMARKS = [
    {
        "event_name": "1950 Assam-Tibet EQ",
        "type": "Earthquake",
        "location": "Assam & Arunachal Pradesh boundary",
        "lat_range": (27.5, 29.5),
        "lng_range": (94.0, 96.5),
        "elevation_m": (500.0, 3500.0),
        "dist_coast_km": (600.0, 900.0),
        "seismic_zone": "Zone V",
        "base_slope": 32.0,
        "magnitude_range": (8.0, 8.6)
    },
    {
        "event_name": "1956 Anjar EQ",
        "type": "Earthquake",
        "location": "Anjar, Kutch, Gujarat",
        "lat_range": (23.0, 24.0),
        "lng_range": (69.5, 70.8),
        "elevation_m": (10.0, 150.0),
        "dist_coast_km": (15.0, 80.0),
        "seismic_zone": "Zone V",
        "base_slope": 8.0,
        "magnitude_range": (6.0, 6.5)
    },
    {
        "event_name": "1961 Panshet Flood",
        "type": "Dam Breach / Flood",
        "location": "Pune, Maharashtra",
        "lat_range": (18.3, 18.7),
        "lng_range": (73.6, 74.0),
        "elevation_m": (550.0, 750.0),
        "dist_coast_km": (90.0, 140.0),
        "seismic_zone": "Zone III",
        "base_slope": 18.0
    },
    {
        "event_name": "1964 Rameswaram Cyclone",
        "type": "Super Cyclone",
        "location": "Dhanushkodi, Tamil Nadu",
        "lat_range": (9.1, 9.4),
        "lng_range": (79.2, 79.5),
        "elevation_m": (1.0, 15.0),
        "dist_coast_km": (0.5, 10.0),
        "seismic_zone": "Zone II",
        "base_slope": 2.0
    },
    {
        "event_name": "1965-66 Great Indian Drought",
        "type": "Pan-Indian Drought",
        "location": "Central & Northern Agricultural Belt",
        "lat_range": (21.0, 28.0),
        "lng_range": (74.0, 82.0),
        "elevation_m": (150.0, 500.0),
        "dist_coast_km": (200.0, 800.0),
        "seismic_zone": "Zone II",
        "base_slope": 5.0
    },
    {
        "event_name": "1967 Koyna EQ",
        "type": "Earthquake",
        "location": "Koynanagar, Maharashtra",
        "lat_range": (17.3, 17.6),
        "lng_range": (73.7, 74.0),
        "elevation_m": (550.0, 850.0),
        "dist_coast_km": (60.0, 90.0),
        "seismic_zone": "Zone IV",
        "base_slope": 28.0,
        "magnitude_range": (6.0, 6.4)
    },
    {
        "event_name": "1968 Darjeeling Landslides",
        "type": "Landslide / Mass Movement",
        "location": "Darjeeling & Jalpaiguri, West Bengal",
        "lat_range": (26.8, 27.2),
        "lng_range": (88.1, 88.6),
        "elevation_m": (800.0, 2200.0),
        "dist_coast_km": (450.0, 550.0),
        "seismic_zone": "Zone IV",
        "base_slope": 38.0
    },
    {
        "event_name": "1970 Alaknanda Flash Flood",
        "type": "Flash Flood / Cloudburst",
        "location": "Alaknanda Valley, Chamoli, Uttarakhand",
        "lat_range": (30.3, 30.7),
        "lng_range": (79.3, 79.8),
        "elevation_m": (1400.0, 3200.0),
        "dist_coast_km": (800.0, 1000.0),
        "seismic_zone": "Zone V",
        "base_slope": 42.0
    },
    {
        "event_name": "1971 Odisha Cyclone",
        "type": "Super Cyclone",
        "location": "Paradip & Kendrapara, Odisha",
        "lat_range": (20.1, 20.6),
        "lng_range": (86.4, 86.9),
        "elevation_m": (2.0, 20.0),
        "dist_coast_km": (1.0, 25.0),
        "seismic_zone": "Zone III",
        "base_slope": 3.0
    },
    {
        "event_name": "1977 Andhra Pradesh Cyclone",
        "type": "Super Cyclone",
        "location": "Diviseema, Andhra Pradesh",
        "lat_range": (15.8, 16.3),
        "lng_range": (80.7, 81.2),
        "elevation_m": (1.0, 12.0),
        "dist_coast_km": (1.0, 20.0),
        "seismic_zone": "Zone III",
        "base_slope": 2.0
    },
    {
        "event_name": "1987 Pan-India Drought",
        "type": "Pan-Indian Drought",
        "location": "Gujarat, Rajasthan, Haryana",
        "lat_range": (23.0, 29.5),
        "lng_range": (70.0, 77.0),
        "elevation_m": (100.0, 450.0),
        "dist_coast_km": (50.0, 600.0),
        "seismic_zone": "Zone II",
        "base_slope": 4.0
    },
    {
        "event_name": "1991 Uttarkashi EQ",
        "type": "Earthquake",
        "location": "Uttarkashi, Uttarakhand",
        "lat_range": (30.6, 31.0),
        "lng_range": (78.3, 78.7),
        "elevation_m": (1100.0, 2800.0),
        "dist_coast_km": (850.0, 1000.0),
        "seismic_zone": "Zone IV",
        "base_slope": 36.0,
        "magnitude_range": (6.5, 7.0)
    },
    {
        "event_name": "1993 Latur EQ",
        "type": "Earthquake",
        "location": "Latur & Osmanabad, Maharashtra",
        "lat_range": (17.9, 18.3),
        "lng_range": (76.4, 76.8),
        "elevation_m": (580.0, 680.0),
        "dist_coast_km": (300.0, 400.0),
        "seismic_zone": "Zone III",
        "base_slope": 10.0,
        "magnitude_range": (6.0, 6.4)
    },
    {
        "event_name": "1999 Odisha Super Cyclone",
        "type": "Super Cyclone",
        "location": "Jagatsinghpur & Paradip, Odisha",
        "lat_range": (20.0, 20.5),
        "lng_range": (86.2, 86.8),
        "elevation_m": (2.0, 15.0),
        "dist_coast_km": (0.5, 15.0),
        "seismic_zone": "Zone III",
        "base_slope": 2.5
    },
    {
        "event_name": "2001 Bhuj EQ",
        "type": "Earthquake",
        "location": "Bhuj, Kutch, Gujarat",
        "lat_range": (23.2, 23.6),
        "lng_range": (69.5, 70.2),
        "elevation_m": (20.0, 200.0),
        "dist_coast_km": (30.0, 100.0),
        "seismic_zone": "Zone V",
        "base_slope": 9.0,
        "magnitude_range": (7.5, 7.9)
    },
    {
        "event_name": "2004 Indian Ocean Tsunami",
        "type": "Tsunami / Megathrust EQ",
        "location": "Tamil Nadu & AP Coast, Andaman Islands",
        "lat_range": (8.0, 13.5),
        "lng_range": (79.5, 93.0),
        "elevation_m": (0.5, 8.0),
        "dist_coast_km": (0.1, 5.0),
        "seismic_zone": "Zone V",
        "base_slope": 1.5
    },
    {
        "event_name": "2005 Mumbai Urban Flood",
        "type": "Extreme Urban Flood",
        "location": "Mumbai & Konkan, Maharashtra",
        "lat_range": (18.9, 19.3),
        "lng_range": (72.8, 73.1),
        "elevation_m": (5.0, 50.0),
        "dist_coast_km": (0.5, 15.0),
        "seismic_zone": "Zone III",
        "base_slope": 8.0
    },
    {
        "event_name": "2005 Kashmir EQ",
        "type": "Earthquake",
        "location": "Uri, Tangdhar, J&K",
        "lat_range": (34.0, 34.6),
        "lng_range": (73.8, 74.4),
        "elevation_m": (1300.0, 3100.0),
        "dist_coast_km": (800.0, 1000.0),
        "seismic_zone": "Zone V",
        "base_slope": 40.0,
        "magnitude_range": (7.3, 7.8)
    },
    {
        "event_name": "2008 Kosi River Flood",
        "type": "Riverine Flood",
        "location": "Supaul & Madhepura, Northern Bihar",
        "lat_range": (25.8, 26.5),
        "lng_range": (86.5, 87.2),
        "elevation_m": (35.0, 75.0),
        "dist_coast_km": (400.0, 500.0),
        "seismic_zone": "Zone IV",
        "base_slope": 6.0
    },
    {
        "event_name": "2010 Leh Cloudburst",
        "type": "Flash Flood / Cloudburst",
        "location": "Leh, Ladakh",
        "lat_range": (34.0, 34.3),
        "lng_range": (77.4, 77.8),
        "elevation_m": (3200.0, 4200.0),
        "dist_coast_km": (900.0, 1100.0),
        "seismic_zone": "Zone IV",
        "base_slope": 35.0
    },
    {
        "event_name": "2013 Uttarakhand GLOF & Floods",
        "type": "GLOF",
        "location": "Kedarnath, Mandakini Valley, Uttarakhand",
        "lat_range": (30.6, 30.9),
        "lng_range": (78.9, 79.3),
        "elevation_m": (2200.0, 3800.0),
        "dist_coast_km": (850.0, 1050.0),
        "seismic_zone": "Zone V",
        "base_slope": 44.0
    },
    {
        "event_name": "2014 Hudhud Cyclone",
        "type": "Tropical Cyclone",
        "location": "Visakhapatnam, Andhra Pradesh",
        "lat_range": (17.5, 17.9),
        "lng_range": (83.1, 83.5),
        "elevation_m": (5.0, 80.0),
        "dist_coast_km": (0.5, 20.0),
        "seismic_zone": "Zone II",
        "base_slope": 12.0
    },
    {
        "event_name": "2015 Chennai Floods",
        "type": "Extreme Urban Flood",
        "location": "Chennai & Kanchipuram, Tamil Nadu",
        "lat_range": (12.8, 13.2),
        "lng_range": (80.0, 80.3),
        "elevation_m": (4.0, 30.0),
        "dist_coast_km": (1.0, 25.0),
        "seismic_zone": "Zone III",
        "base_slope": 3.0
    },
    {
        "event_name": "2018 Kerala Floods",
        "type": "Extreme Flood / Landslides",
        "location": "Idukki, Wayanad & Central Kerala",
        "lat_range": (9.2, 11.8),
        "lng_range": (76.2, 77.2),
        "elevation_m": (50.0, 1800.0),
        "dist_coast_km": (15.0, 120.0),
        "seismic_zone": "Zone III",
        "base_slope": 38.0
    },
    {
        "event_name": "2020 Cyclone Amphan",
        "type": "Super Cyclone",
        "location": "Sundarbans & Kolkata, West Bengal",
        "lat_range": (21.5, 22.6),
        "lng_range": (88.0, 89.2),
        "elevation_m": (2.0, 12.0),
        "dist_coast_km": (0.5, 60.0),
        "seismic_zone": "Zone III",
        "base_slope": 2.0
    },
    {
        "event_name": "2021 Chamoli GLOF",
        "type": "GLOF",
        "location": "Raini, Chamoli, Uttarakhand",
        "lat_range": (30.4, 30.6),
        "lng_range": (79.6, 79.9),
        "elevation_m": (2400.0, 4800.0),
        "dist_coast_km": (850.0, 1050.0),
        "seismic_zone": "Zone V",
        "base_slope": 46.0
    },
    {
        "event_name": "2021 Cyclone Tauktae",
        "type": "Tropical Cyclone",
        "location": "Saurashtra Coast, Gujarat",
        "lat_range": (20.5, 21.5),
        "lng_range": (70.5, 71.8),
        "elevation_m": (5.0, 60.0),
        "dist_coast_km": (0.5, 40.0),
        "seismic_zone": "Zone III",
        "base_slope": 6.0
    },
    {
        "event_name": "2023 Joshimath Subsidence",
        "type": "Land Subsidence",
        "location": "Joshimath, Chamoli, Uttarakhand",
        "lat_range": (30.52, 30.58),
        "lng_range": (79.54, 79.60),
        "elevation_m": (1800.0, 2200.0),
        "dist_coast_km": (850.0, 1000.0),
        "seismic_zone": "Zone V",
        "base_slope": 34.0
    },
    {
        "event_name": "2023 Cyclone Biparjoy",
        "type": "Tropical Cyclone",
        "location": "Jakhau, Kutch, Gujarat",
        "lat_range": (22.8, 23.5),
        "lng_range": (68.5, 69.8),
        "elevation_m": (2.0, 40.0),
        "dist_coast_km": (0.5, 30.0),
        "seismic_zone": "Zone V",
        "base_slope": 4.0
    },
    {
        "event_name": "2024 Wayanad Landslides",
        "type": "Landslide / Mass Movement",
        "location": "Chooralmala, Mundakkai, Wayanad, Kerala",
        "lat_range": (11.5, 11.7),
        "lng_range": (76.1, 76.3),
        "elevation_m": (700.0, 1500.0),
        "dist_coast_km": (60.0, 90.0),
        "seismic_zone": "Zone III",
        "base_slope": 42.0
    },
    {
        "event_name": "2025 Central-West Deluge",
        "type": "Riverine Flood",
        "location": "Vadodara & Jamnagar, Gujarat",
        "lat_range": (22.0, 22.8),
        "lng_range": (70.0, 73.5),
        "elevation_m": (15.0, 80.0),
        "dist_coast_km": (10.0, 80.0),
        "seismic_zone": "Zone III",
        "base_slope": 5.0
    }
]

def classify_imd_severity(mm: float, disaster_type: str) -> str:
    """Classifies severity based on IMD precipitation and disaster magnitude scales."""
    if disaster_type == "Earthquake":
        return "N/A (Seismic)"
    elif disaster_type == "Pan-Indian Drought":
        return "Severe Monsoon Deficit"
    
    if mm < 64.4:
        return "Moderate Rain"
    elif mm < 115.5:
        return "Heavy"
    elif mm < 204.4:
        return "Very Heavy"
    elif mm < 400.0:
        return "Extremely Heavy"
    else:
        return "Cloudburst / Catastrophic"

def determine_intensity_regime(hourly_peak_mm: float, disaster_type: str, wind_speed_kmh: float) -> str:
    """Categorizes peak intensity into meteorological/hazard regimes."""
    if disaster_type == "Earthquake":
        return "Seismic Rupture Regime"
    elif disaster_type in ["Super Cyclone", "Tropical Cyclone"]:
        if wind_speed_kmh > 200:
            return "Catastrophic Cyclonic Surge"
        elif wind_speed_kmh > 120:
            return "Severe Cyclonic Wind Regime"
        else:
            return "Moderate Cyclonic Depression"
    elif disaster_type == "Pan-Indian Drought":
        return "Extended Drought Regime"
    
    if hourly_peak_mm < 30.0:
        return "Normal Monsoon Regime"
    elif hourly_peak_mm <= 75.0:
        return "Urban Inundation Threshold"
    else:
        return "Cloudburst Flash Flood Regime"

def generate_disaster_dataset(n_samples: int = 30000, output_dir: str = None) -> pd.DataFrame:
    """
    Generates synthetic 1950-2026 disaster dataset grounded in report benchmarks.
    """
    print(f"Generating {n_samples:,} synthetic historical disaster records (1950-2026)...")

    records = []
    
    # Non-stationarity weight distribution across 1950-2026 timeline
    years = np.random.randint(1950, 2027, size=n_samples)
    
    # Pre-generate distributions
    # 24h precipitation GEV distribution
    gev_rain = np.clip(genextreme.rvs(c=-0.35, loc=180.0, scale=90.0, size=n_samples), 0.0, 1100.0)
    
    # Log-normal monthly departure
    departure_pct = np.clip(np.random.lognormal(mean=4.5, sigma=0.6, size=n_samples), 5.0, 1400.0)

    for i in range(n_samples):
        event_id = i + 1
        year = int(years[i])
        
        # Select benchmark archetype
        benchmark = random.choice(HISTORICAL_BENCHMARKS)
        dtype = benchmark["type"]
        bench_name = benchmark["event_name"]
        
        # Spatial Coordinates
        lat = round(random.uniform(benchmark["lat_range"][0], benchmark["lat_range"][1]), 4)
        lng = round(random.uniform(benchmark["lng_range"][0], benchmark["lng_range"][1]), 4)
        elevation = round(random.uniform(benchmark["elevation_m"][0], benchmark["elevation_m"][1]), 1)
        dist_coast = round(max(0.5, random.uniform(benchmark["dist_coast_km"][0], benchmark["dist_coast_km"][1])), 1)
        seismic_zone = benchmark["seismic_zone"]
        slope_deg = round(max(1.0, benchmark["base_slope"] + random.uniform(-5.0, 5.0)), 1)
        
        # Post-2000 climate non-stationarity multipliers
        climate_shift_mult = 1.0 + max(0.0, (year - 2000) * 0.015)

        # Environmental & Meteorological variables initialized by hazard type
        if dtype == "Earthquake":
            p24_mm = round(float(random.uniform(0.0, 45.0)), 2)
            monthly_dep = round(float(random.uniform(10.0, 100.0)), 2)
            hourly_peak = round(float(p24_mm * random.uniform(0.05, 0.2)), 2)
            oni_index = round(random.uniform(-1.5, 1.5), 2)
            sst_anomaly = round(random.uniform(-0.5, 0.8), 2)
            wind_speed = round(random.uniform(5.0, 35.0), 1)
            soil_sat = round(random.uniform(0.1, 0.6), 3)
            river_level_m = round(random.uniform(0.5, 3.5), 2)
            danger_m = round(random.uniform(5.0, 12.0), 2)
            
        elif dtype in ["Super Cyclone", "Tropical Cyclone"]:
            # High wind, high SST, close to coast
            dist_coast = round(min(145.0, dist_coast), 1)
            sst_anomaly = round(random.uniform(0.8, 2.8) * (1.1 if year > 2010 else 1.0), 2)
            oni_index = round(random.uniform(-1.0, 2.2), 2)
            
            p24_mm = round(float(np.clip(gev_rain[i] * 1.3 * climate_shift_mult, 120.0, 950.0)), 2)
            monthly_dep = round(float(departure_pct[i] * 1.2), 2)
            hourly_peak = round(float(p24_mm * random.uniform(0.25, 0.45)), 2)
            
            base_wind = 210.0 if dtype == "Super Cyclone" else 135.0
            wind_speed = round(float(base_wind + random.uniform(-25.0, 55.0)), 1)
            soil_sat = round(min(1.0, 0.65 + p24_mm / 1000.0), 3)
            
            danger_m = round(random.uniform(4.0, 15.0), 2)
            river_level_m = round(danger_m + random.uniform(1.2, 5.5), 2)
            
        elif dtype == "Pan-Indian Drought":
            # High positive ENSO (El Nino), low rain, low departure
            oni_index = round(random.uniform(0.8, 2.5), 2)
            sst_anomaly = round(random.uniform(-0.5, 1.2), 2)
            p24_mm = round(float(random.uniform(0.0, 35.0)), 2)
            monthly_dep = round(float(random.uniform(5.0, 45.0)), 2) # severe deficit < 50%
            hourly_peak = round(float(random.uniform(0.0, 10.0)), 2)
            wind_speed = round(random.uniform(10.0, 40.0), 1)
            soil_sat = round(random.uniform(0.05, 0.25), 3)
            danger_m = round(random.uniform(5.0, 20.0), 2)
            river_level_m = round(max(0.2, danger_m - random.uniform(2.5, 4.5)), 2)
            
        elif dtype == "GLOF":
            # High elevation (> 2000m), steep slope (> 30)
            elevation = round(max(2050.0, elevation), 1)
            slope_deg = round(max(32.0, slope_deg), 1)
            oni_index = round(random.uniform(-1.5, 1.5), 2)
            sst_anomaly = round(random.uniform(0.2, 1.8), 2)
            
            p24_mm = round(float(np.clip(gev_rain[i] * 1.1, 150.0, 800.0)), 2)
            monthly_dep = round(float(departure_pct[i]), 2)
            hourly_peak = round(float(p24_mm * random.uniform(0.35, 0.55)), 2) # high hourly spike
            wind_speed = round(random.uniform(20.0, 70.0), 1)
            soil_sat = round(random.uniform(0.70, 0.98), 3)
            danger_m = round(random.uniform(8.0, 16.0), 2)
            river_level_m = round(danger_m + random.uniform(2.0, 7.0), 2)
            
        else: # Floods, Cloudbursts, Landslides, Subsidence
            oni_index = round(random.uniform(-1.8, 1.8), 2)
            sst_anomaly = round(random.uniform(-0.2, 1.5), 2)
            
            p24_mm = round(float(np.clip(gev_rain[i] * climate_shift_mult, 80.0, 1000.0)), 2)
            monthly_dep = round(float(departure_pct[i]), 2)
            
            is_cloudburst = (p24_mm >= 350.0) or (dtype in ["Flash Flood / Cloudburst", "GLOF"])
            intensity_ratio = random.uniform(0.35, 0.55) if is_cloudburst else random.uniform(0.15, 0.35)
            hourly_peak = round(float(p24_mm * intensity_ratio), 2)
            
            wind_speed = round(random.uniform(15.0, 85.0), 1)
            soil_sat = round(min(1.0, max(0.2, (p24_mm / 300.0) * 0.65 + (monthly_dep / 350.0) * 0.35)), 3)
            
            danger_m = round(random.uniform(5.0, 210.0), 2)
            river_level_m = round(danger_m + random.uniform(-1.0, 4.5), 2)

        # Vegetation NDVI
        ndvi = round(max(0.05, min(0.85, 0.50 + random.uniform(-0.35, 0.30))), 2)

        # IMD and Intensity Classification
        imd_category = classify_imd_severity(p24_mm, dtype)
        intensity_regime = determine_intensity_regime(hourly_peak, dtype, wind_speed)
        
        danger_departure = round(river_level_m - danger_m, 2)

        # ---------------------------------------------------------------------
        # Ground Truth Cascade Probability & Target Calculation
        # ---------------------------------------------------------------------
        if dtype == "Earthquake":
            mag = benchmark.get("magnitude_range", (6.0, 7.5))
            eq_mag = random.uniform(mag[0], mag[1])
            z = (eq_mag - 6.2) / 0.6 + (slope_deg - 20.0) / 10.0
        elif dtype in ["Super Cyclone", "Tropical Cyclone"]:
            z = (wind_speed - 120.0) / 30.0 + (p24_mm - 150.0) / 60.0 + (100.0 - dist_coast) / 30.0
        elif dtype == "Pan-Indian Drought":
            z = (oni_index - 1.0) / 0.5 + (50.0 - monthly_dep) / 15.0
        else:
            z = (p24_mm - 180.0) / 50.0 + (danger_departure) / 1.5 + (soil_sat - 0.7) / 0.15 + (slope_deg - 25.0) / 12.0

        prob_target = 1.0 / (1.0 + math.exp(-z))
        prob_target = float(np.clip(prob_target + np.random.normal(0, 0.025), 0.01, 0.99))
        prob_target = round(prob_target, 4)

        # Lead time calculation
        if dtype == "Earthquake":
            lead_time_target = round(random.uniform(5.0, 25.0), 1)
        elif dtype in ["Super Cyclone", "Tropical Cyclone"]:
            lead_time_target = round(float(np.clip(180.0 - (wind_speed * 0.4), 30.0, 180.0)), 1)
        else:
            lead_time_target = round(float(np.clip(120.0 - (prob_target * 90.0) + random.uniform(-4.0, 4.0), 15.0, 180.0)), 1)

        # Risk level classification
        if prob_target >= 0.75:
            risk_level = "Critical" if (dtype in ["Super Cyclone", "GLOF"] or p24_mm > 500.0) else "High"
            secondary_hazard = "Massive Landslide & Inundation" if slope_deg > 30.0 else "Severe Coastal/Urban Deluge"
        elif prob_target >= 0.40:
            risk_level = "Medium"
            secondary_hazard = "Slope Instability / Debris Flow" if slope_deg > 20.0 else "River Swell & Drainage Overflow"
        else:
            risk_level = "Low"
            secondary_hazard = "None"

        records.append({
            "Synthetic_Event_ID": event_id,
            "Year": year,
            "Disaster_Type": dtype,
            "Historical_Benchmark_Ref": bench_name,
            "Primary_Location": benchmark["location"],
            "Latitude": lat,
            "Longitude": lng,
            "Elevation_m": elevation,
            "Distance_to_Coast_km": dist_coast,
            "Seismic_Zone": seismic_zone,
            "Terrain_Slope_Deg": slope_deg,
            "Peak_24h_Rainfall_mm": p24_mm,
            "Monthly_Monsoon_Departure_Pct": monthly_dep,
            "Peak_Hourly_Intensity_mm_hr": hourly_peak,
            "ENSO_ONI_Index": oni_index,
            "SST_Anomaly_C": sst_anomaly,
            "Max_Wind_Speed_kmh": wind_speed,
            "Soil_Saturation_Index": soil_sat,
            "Vegetation_NDVI": ndvi,
            "River_Level_m": river_level_m,
            "River_Danger_Level_m": danger_m,
            "River_Danger_Departure_m": danger_departure,
            "IMD_Severity_Category": imd_category,
            "Intensity_Regime": intensity_regime,
            "Cascade_Probability": prob_target,
            "Estimated_Lead_Time_Mins": lead_time_target,
            "Risk_Level": risk_level,
            "Secondary_Cascade_Hazard": secondary_hazard
        })

    df = pd.DataFrame(records)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        csv_path = os.path.join(output_dir, "disaster_synthetic_dataset_1950_2026.csv")
        json_path = os.path.join(output_dir, "disaster_synthetic_dataset_1950_2026.json")
        
        df.to_csv(csv_path, index=False)
        df.to_json(json_path, orient="records", indent=2)
        print(f"[OK] Successfully saved 30,000 synthetic disaster records:")
        print(f"   - CSV:  {csv_path} ({os.path.getsize(csv_path) / (1024*1024):.2f} MB)")
        print(f"   - JSON: {json_path} ({os.path.getsize(json_path) / (1024*1024):.2f} MB)")

    return df

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "datasets")
    df = generate_disaster_dataset(n_samples=30000, output_dir=output_dir)
    print("\nDataset Summary Statistics:")
    print(df[["Year", "Peak_24h_Rainfall_mm", "Max_Wind_Speed_kmh", "Cascade_Probability", "Estimated_Lead_Time_Mins"]].describe())
    print("\nSample Data (First 5 Rows):")
    print(df.head(5))
