"""
[OPTIMIZED GRAPH FEATURE BUILDER] Normalizes input node features for fast model convergence.
Applies Z-score scaling to rain, elevation, slope, and river gauge features.
"""
from typing import List, Dict, Any, Tuple
import math

try:
    import torch
    from torch_geometric.data import Data
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

# Feature mean and std constants for fast z-score normalization
FEATURE_MEANS = [75.0, 3.5, 30.0, 60.0, 2000.0, 0.50]
FEATURE_STDS  = [50.0, 2.5, 12.0, 20.0, 500.0,  0.20]

def normalize_features(raw_features: List[List[float]]) -> List[List[float]]:
    """Applies Z-score normalization: (x - mean) / std to ensure rapid gradient descent convergence."""
    normalized = []
    for row in raw_features:
        norm_row = []
        for i in range(len(row)):
            val = (row[i] - FEATURE_MEANS[i]) / FEATURE_STDS[i]
            norm_row.append(round(val, 4))
        normalized.append(norm_row)
    return normalized

class SpatialGraphBuilder:
    def __init__(self):
        pass

    def build_spatial_grid_graph(self, center_lat: float, center_lng: float, rainfall_mm: float, river_level_m: float = 0.0) -> Any:
        """
        Constructs a 5-node spatial neighborhood graph with normalized features:
        Node 0: Target location (center)
        Nodes 1-4: Upstream terrain slopes & river sensors
        """
        # Raw Node features: [rainfall_mm, river_level_m, slope_angle_deg, soil_moisture_pct, elevation_m, vegetation_ndvi]
        raw_features = [
            [rainfall_mm, river_level_m or 0.0, 38.5, 82.0, 2200.0, 0.45],          # Node 0 (Target)
            [rainfall_mm * 1.1, river_level_m * 1.2, 42.0, 88.0, 2600.0, 0.35],      # Node 1 (Upstream High Slope)
            [rainfall_mm * 0.9, river_level_m * 0.9, 25.0, 70.0, 1900.0, 0.60],      # Node 2 (Downstream Valley)
            [rainfall_mm * 1.05, river_level_m * 1.0, 35.0, 80.0, 2400.0, 0.40],     # Node 3 (Adjacent Ridge)
            [rainfall_mm * 0.95, river_level_m * 0.8, 18.0, 65.0, 1750.0, 0.70]      # Node 4 (Relief Station Base)
        ]

        norm_features = normalize_features(raw_features)

        # Edge connections (Source -> Target directed flow)
        edges = [
            [1, 0], [3, 0], [0, 2], [2, 4], [1, 3], [3, 2]
        ]
        
        if TORCH_AVAILABLE:
            x_tensor = torch.tensor(norm_features, dtype=torch.float)
            edge_index_tensor = torch.tensor(edges, dtype=torch.long).t().contiguous()
            return Data(x=x_tensor, edge_index=edge_index_tensor)
        else:
            return {
                "node_features": norm_features,
                "edge_index": edges
            }
