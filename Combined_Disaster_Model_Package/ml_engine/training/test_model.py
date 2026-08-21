"""
[COMPREHENSIVE GAT MODEL TEST SUITE]
Evaluates trained PyTorch GATCascadeNet model on held-out test datasets, 
historical benchmark disaster events, and quantitative metrics (BCE, MAE, R2).
"""
import os
import torch
import numpy as np
import pandas as pd
import torch.nn as nn
from torch_geometric.loader import DataLoader
from ml_engine.inference import CascadePredictor
from ml_engine.models.gat_cascade import GATCascadeNet
from ml_engine.training.train import load_hydrological_training_batch

# Historical Event Benchmark Test Cases from 2000-2026 Quantitative Report
HISTORICAL_TEST_CASES = [
    {
        "event": "Mumbai Santa Cruz (2005)",
        "rain_mm": 944.0,
        "river_m": 8.5,
        "region": "Urban Coastal",
        "expected_risk": "High"
    },
    {
        "event": "Kedarnath Cloudburst (2013)",
        "rain_mm": 326.0,
        "river_m": 16.2,
        "region": "Alpine Himalayan",
        "expected_risk": "High"
    },
    {
        "event": "Chennai Northeast Monsoon (2015)",
        "rain_mm": 494.0,
        "river_m": 6.8,
        "region": "Coastal Urban",
        "expected_risk": "High"
    },
    {
        "event": "Peermade Kerala (2018)",
        "rain_mm": 398.0,
        "river_m": 12.0,
        "region": "Western Ghats",
        "expected_risk": "High"
    },
    {
        "event": "Mahad Chiplun Floods (2021)",
        "rain_mm": 590.0,
        "river_m": 11.8,
        "region": "Konkan Escarpment",
        "expected_risk": "High"
    },
    {
        "event": "Wayanad Saturation Landslide (2024)",
        "rain_mm": 356.0,
        "river_m": 9.2,
        "region": "Highland Ghats",
        "expected_risk": "High"
    },
    {
        "event": "Leh High-Altitude Cloudburst (2010)",
        "rain_mm": 250.0,
        "river_m": 4.5,
        "region": "Ladakh Plateau",
        "expected_risk": "High"
    },
    {
        "event": "Normal Dry Season Baseline",
        "rain_mm": 12.5,
        "river_m": 1.2,
        "region": "Deccan Plateau",
        "expected_risk": "Low"
    },
    {
        "event": "Moderate Pre-Monsoon Showers",
        "rain_mm": 45.0,
        "river_m": 2.1,
        "region": "Gangetic Plains",
        "expected_risk": "Low"
    }
]

def run_comprehensive_tests():
    print("=" * 75)
    print("      GAT CASCADE MODEL COMPREHENSIVE TESTING & EVALUATION REPORT")
    print("=" * 75)
    
    # 1. Load Trained Weights & Model
    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    weights_path = os.path.join(models_dir, "gat_cascade_v1.pt")
    
    if not os.path.exists(weights_path):
        print(f"Error: Weights file not found at {weights_path}")
        return

    model = GATCascadeNet(in_channels=6)
    model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu')))
    model.eval()
    print(f"Loaded trained GATCascadeNet model weights from:\n  {weights_path}\n")

    # 2. Quantitative Evaluation on Held-Out 2,000 Graph Test Split
    print("--- 1. Quantitative Performance Metrics (2,000 Graph Held-Out Test Set) ---")
    dataset = load_hydrological_training_batch(num_graphs=10000)
    split_idx = int(len(dataset) * 0.8)
    test_graphs = [item[0] for item in dataset[split_idx:]]
    test_loader = DataLoader(test_graphs, batch_size=128, shuffle=False)

    bce_loss_fn = nn.BCELoss()
    mse_loss_fn = nn.MSELoss()

    actual_probs, pred_probs = [], []
    actual_lts, pred_lts = [], []

    total_bce, total_mse = 0.0, 0.0
    with torch.no_grad():
        for batch in test_loader:
            pred_p_all, pred_lt_all, _ = model(batch.x, batch.edge_index)
            target_indices = batch.ptr[:-1]
            
            p_pred = pred_p_all[target_indices]
            lt_pred = pred_lt_all[target_indices]
            
            bce = bce_loss_fn(p_pred, batch.y_prob).item()
            mse = mse_loss_fn(lt_pred, batch.y_lt).item()
            
            total_bce += bce * batch.num_graphs
            total_mse += mse * batch.num_graphs
            
            actual_probs.extend(batch.y_prob.view(-1).tolist())
            pred_probs.extend(p_pred.view(-1).tolist())
            actual_lts.extend(batch.y_lt.view(-1).tolist())
            pred_lts.extend(lt_pred.view(-1).tolist())

    actual_probs = np.array(actual_probs)
    pred_probs = np.array(pred_probs)
    actual_lts = np.array(actual_lts)
    pred_lts = np.array(pred_lts)

    avg_bce = total_bce / len(test_graphs)
    prob_mae = np.mean(np.abs(actual_probs - pred_probs))
    
    # Classification Accuracy threshold at 0.50
    correct_class = np.sum((actual_probs >= 0.50) == (pred_probs >= 0.50))
    accuracy = (correct_class / len(actual_probs)) * 100.0
    
    # Lead time MAE (mins)
    lt_mae = np.mean(np.abs(actual_lts - pred_lts))

    print(f"  - BCE Loss (Probability)    : {avg_bce:.4f}")
    print(f"  - Probability MAE           : {prob_mae:.4f}")
    print(f"  - Classification Accuracy    : {accuracy:.2f}%")
    print(f"  - Lead Time MAE             : {lt_mae:.2f} mins\n")

    # 3. Test Historical Case Scenarios using CascadePredictor API
    print("--- 2. Historical Case Scenario Benchmark Tests ---")
    predictor = CascadePredictor()
    
    print(f"{'Event Scenario':<36} | {'Rain (mm)':<9} | {'River (m)':<9} | {'Pred Prob':<9} | {'Lead Time':<10} | {'Risk Level'}")
    print("-" * 95)
    
    for case in HISTORICAL_TEST_CASES:
        res = predictor.predict_cascade_hazard(
            latitude=28.6,
            longitude=77.2,
            rainfall_mm=case["rain_mm"],
            river_level_m=case["river_m"],
            district_id=case["event"]
        )
        prob_str = f"{res['cascade_probability']:.2f}"
        lt_str = f"{res['estimated_lead_time_mins']} min"
        print(f"{case['event']:<36} | {case['rain_mm']:<9.1f} | {case['river_m']:<9.1f} | {prob_str:<9} | {lt_str:<10} | {res['risk_level']}")

    print("=" * 75)

if __name__ == "__main__":
    run_comprehensive_tests()
