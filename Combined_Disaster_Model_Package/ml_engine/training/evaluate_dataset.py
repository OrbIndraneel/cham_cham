"""
[DISASTER METEOROLOGICAL DATASET EVALUATOR & VERIFIER]
Validates the synthetic disaster dataset (1950-2026) properties and evaluates GAT cascade predictions.
"""
import os
import pandas as pd
import numpy as np
from ml_engine.data.generate_disaster_dataset_1950_2026 import generate_disaster_dataset
from ml_engine.inference import CascadePredictor

def evaluate_dataset_statistics(dataset_path: str = None):
    if dataset_path is None:
        dataset_path = os.path.join(os.path.dirname(__file__), "..", "data", "datasets", "disaster_synthetic_dataset_1950_2026.csv")
    
    if not os.path.exists(dataset_path):
        print("Generating 30,000 benchmark dataset...")
        df = generate_disaster_dataset(30000, output_dir=os.path.dirname(dataset_path))
    else:
        df = pd.read_csv(dataset_path)

    print("=" * 75)
    print("HISTORICAL DISASTER SYNTHETIC BENCHMARK DATASET VERIFICATION (1950-2026)")
    print("=" * 75)
    print(f"Total Synthetic Records: {len(df):,}")
    print(f"Time Horizon           : {df['Year'].min()} - {df['Year'].max()}")
    if 'Disaster_Type' in df.columns:
        print(f"Disaster Types Covered : {df['Disaster_Type'].nunique()} Unique Hazard Types")
    
    print("\n--- Quantitative Parameter Checks ---")
    print(f"Mean Peak 24h Rain     : {df['Peak_24h_Rainfall_mm'].mean():.2f} mm")
    print(f"Max Single-Day Rain    : {df['Peak_24h_Rainfall_mm'].max():.2f} mm")
    print(f"Mean Max Wind Speed    : {df['Max_Wind_Speed_kmh'].mean():.2f} km/h")
    print(f"Mean Peak Intensity    : {df['Peak_Hourly_Intensity_mm_hr'].mean():.2f} mm/hr")
    if 'ENSO_ONI_Index' in df.columns:
        print(f"ENSO ONI Index Range   : {df['ENSO_ONI_Index'].min():.2f} to {df['ENSO_ONI_Index'].max():.2f}")

    if 'Disaster_Type' in df.columns:
        print("\n--- Multi-Hazard Disaster Type Distribution ---")
        type_counts = df['Disaster_Type'].value_counts()
        for dtype, count in type_counts.items():
            pct = (count / len(df)) * 100
            print(f"  - {dtype:<30}: {count:6,} ({pct:5.1f}%)")

    print("\n--- IMD Severity Distribution ---")
    severity_counts = df['IMD_Severity_Category'].value_counts()
    for cat, count in severity_counts.items():
        pct = (count / len(df)) * 100
        print(f"  - {cat:<26}: {count:6,} ({pct:5.1f}%)")

    print("\n--- Risk Level Distribution ---")
    risk_counts = df['Risk_Level'].value_counts()
    for rk, count in risk_counts.items():
        pct = (count / len(df)) * 100
        print(f"  - {rk:<10}: {count:6,} ({pct:5.1f}%)")

    print("\n--- Running Sample Inference Verification ---")
    predictor = CascadePredictor()
    sample_events = df.sample(3, random_state=101)
    for idx, row in sample_events.iterrows():
        lat = float(row['Latitude']) if 'Latitude' in row else 28.6139
        lng = float(row['Longitude']) if 'Longitude' in row else 77.2090
        res = predictor.predict_cascade_hazard(
            latitude=lat,
            longitude=lng,
            rainfall_mm=float(row['Peak_24h_Rainfall_mm']),
            river_level_m=float(row['River_Level_m']),
            district_id=f"DISASTER_{row['Synthetic_Event_ID']}"
        )
        loc_str = row['Primary_Location'] if 'Primary_Location' in row else row.get('River_Basin', 'Location')
        dtype_str = row.get('Disaster_Type', 'Hazard')
        print(f"\n[Event ID {row['Synthetic_Event_ID']} - {dtype_str} @ {loc_str}]")
        print(f"  Rain: {row['Peak_24h_Rainfall_mm']} mm | Wind: {row.get('Max_Wind_Speed_kmh', 'N/A')} km/h | Target Prob: {row['Cascade_Probability']}")
        print(f"  Predicted Cascade Prob: {res['cascade_probability']} | Predicted Lead Time: {res['estimated_lead_time_mins']} min | Risk: {res['risk_level']}")

    print("=" * 75)

if __name__ == "__main__":
    evaluate_dataset_statistics()

