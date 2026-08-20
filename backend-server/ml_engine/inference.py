"""
[GAT INFERENCE ENGINE] High-speed prediction inference engine.
Loads trained weights (gat_cascade_v1.pt) and evaluates compound cascade probabilities & hazard polygons.
"""
import os
import json
from typing import Dict, Any, List
from ml_engine.models.gat_cascade import GATCascadeNet, TORCH_AVAILABLE
from ml_engine.feature_engineering.graph_builder import SpatialGraphBuilder

class CascadePredictor:
    def __init__(self):
        self.graph_builder = SpatialGraphBuilder()
        self.model = None
        self.is_loaded = False
        self._load_weights()

    def _load_weights(self):
        """Loads trained PyTorch GAT model weights if available."""
        models_dir = os.path.join(os.path.dirname(__file__), "models")
        weights_path = os.path.join(models_dir, "gat_cascade_v1.pt")
        
        if TORCH_AVAILABLE and os.path.exists(weights_path):
            try:
                import torch
                self.model = GATCascadeNet(in_channels=6)
                self.model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu')))
                self.model.eval()
                self.is_loaded = True
            except Exception as e:
                print(f"Notice: Failed loading GAT weights: {e}")
                self.model = GATCascadeNet(in_channels=6)
        else:
            self.model = GATCascadeNet(in_channels=6)

    def predict_cascade_hazard(
        self,
        latitude: float,
        longitude: float,
        rainfall_mm: float,
        river_level_m: float = 0.0,
        district_id: str = "DIST_01"
    ) -> Dict[str, Any]:
        """
        Runs GAT model inference on target location.
        Returns cascade_probability, lead_time_mins, risk_level, and risk polygon coordinates.
        """
        # 1. Build Spatial Graph Data
        graph_data = self.graph_builder.build_spatial_grid_graph(latitude, longitude, rainfall_mm, river_level_m)
        
        # 2. Run Forward Pass Inference
        if TORCH_AVAILABLE and self.is_loaded:
            import torch
            with torch.no_grad():
                pred_prob, pred_lead_time, pred_logits = self.model(graph_data.x, graph_data.edge_index)
                
                prob_val = float(pred_prob[0].item())
                lead_time_val = int(pred_lead_time[0].item())
                
                prob = round(prob_val, 2)
                lead_time = max(15, min(120, lead_time_val))
                
                if prob >= 0.70:
                    risk = "High"
                    secondary = "Landslide & Flash Flood"
                elif prob >= 0.40:
                    risk = "Medium"
                    secondary = "Debris Flow"
                else:
                    risk = "Low"
                    secondary = "None"
        else:
            # Fallback heuristic prediction
            res = self.model.predict_heuristic(rainfall_mm, river_level_m)
            prob = res["cascade_probability"]
            lead_time = res["estimated_lead_time_mins"]
            risk = res["risk_level"]
            secondary = "Landslide & Flash Flood" if risk == "High" else ("Debris Flow" if risk == "Medium" else "None")

        # 3. Construct Risk Polygon Coordinates around Target
        offset = 0.018 if risk == "High" else (0.010 if risk == "Medium" else 0.005)
        polygon_coords = [
            [round(latitude + offset, 4), round(longitude - offset, 4)],
            [round(latitude + offset, 4), round(longitude + offset, 4)],
            [round(latitude - offset, 4), round(longitude + offset, 4)],
            [round(latitude - offset, 4), round(longitude - offset, 4)]
        ]

        return {
            "district_id": district_id,
            "primary_hazard": "Heavy Rainfall" if rainfall_mm >= 50.0 else "Light Rainfall",
            "secondary_cascade_hazard": secondary,
            "cascade_probability": prob,
            "estimated_lead_time_mins": lead_time,
            "risk_level": risk,
            "affected_population_estimate": 14500 if risk == "High" else (4200 if risk == "Medium" else 300),
            "severity_score": round(prob * 10.0, 1),
            "soil_saturation_index": round(min(1.0, rainfall_mm / 150.0), 2),
            "polygon_coordinates": polygon_coords
        }
