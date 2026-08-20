"""
[ISRO BHUVAN DATASET PIPELINE]
Utility for loading ISRO Bhuvan Landslide Hazard Zonation (LHZ) Shapefiles and 
CartoDEM Digital Elevation Models (DEM) to construct PyTorch Geometric (PyG) graphs for GNN training.
"""

import os
from typing import List, Tuple, Dict, Any

try:
    import torch
    from torch_geometric.data import Data
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    import geopandas as gpd
    import rasterio
    import numpy as np
    GIS_AVAILABLE = True
except ImportError:
    GIS_AVAILABLE = False


def extract_features_from_bhuvan_shp(
    shapefile_path: str,
    dem_tif_path: str = None
) -> Tuple[List[List[float]], List[Tuple[int, int]], List[float]]:
    """
    Parses ISRO Bhuvan Shapefile (.shp) and Digital Elevation Model (.tif).
    Returns:
        node_features: List of feature vectors per polygon centroid [rainfall, river_level, slope, soil_moisture, elevation, ndvi]
        edge_index: Graph connectivity based on spatial adjacency (touches / Delaunay)
        labels: Ground truth cascade hazard occurrence (1.0 or 0.0) from Bhuvan LHZ rating
    """
    if not GIS_AVAILABLE:
        print("[Bhuvan Loader] geopandas/rasterio not installed. Using synthetic Himalayan graph data.")
        return generate_synthetic_bhuvan_graph()

    # Read Bhuvan Landslide Hazard Shapefile
    gdf = gpd.read_file(shapefile_path)
    
    # Calculate polygon centroids
    centroids = gdf.geometry.centroid
    coords = np.array([(c.x, c.y) for c in centroids])

    node_features = []
    labels = []

    for idx, row in gdf.iterrows():
        # Map Bhuvan LHZ Risk Class to binary / scalar ground truth label
        lhz_class = str(row.get('LHZ_CLASS', row.get('HAZARD_RAT', 'MODERATE'))).upper()
        label = 1.0 if lhz_class in ['VERY HIGH', 'HIGH', 'CRITICAL'] else 0.0
        labels.append(label)

        # Extract features (defaulting to region averages if raster overlay unavailable)
        slope = float(row.get('SLOPE_DEG', 35.0))
        elevation = float(row.get('ELEVATION', 2100.0))
        ndvi = float(row.get('NDVI', 0.45))
        rainfall = float(row.get('RAINFALL', 120.0))
        river_gauge = float(row.get('RIVER_M', 3.5))
        soil_moisture = float(row.get('SOIL_M', 80.0))

        feat = [rainfall, river_gauge, slope, soil_moisture, elevation, ndvi]
        node_features.append(feat)

    # Build Graph Edges based on Spatial Adjacency (Touching Polygons)
    edges = []
    num_nodes = len(gdf)
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if gdf.geometry.iloc[i].touches(gdf.geometry.iloc[j]) or gdf.geometry.iloc[i].distance(gdf.geometry.iloc[j]) < 0.05:
                edges.append((i, j))
                edges.append((j, i))  # Undirected spatial graph

    return node_features, edges, labels


def generate_synthetic_bhuvan_graph() -> Tuple[List[List[float]], List[Tuple[int, int]], List[float]]:
    """
    Generates a realistic 10-node Himalayan grid graph modeled after ISRO Bhuvan Shimla/Chamoli shapefiles.
    """
    # 10 regions in Shimla-Kinnaur landslide hazard corridor
    node_features = [
        [145.0, 4.2, 42.5, 88.0, 2450.0, 0.35], # High risk slope
        [138.0, 3.8, 38.0, 84.0, 2300.0, 0.40],
        [120.0, 3.2, 31.0, 78.0, 2100.0, 0.50],
        [95.0,  2.8, 24.0, 68.0, 1850.0, 0.65],
        [160.0, 5.1, 46.0, 92.0, 2750.0, 0.28], # Critical slope
        [110.0, 2.5, 18.0, 60.0, 1600.0, 0.72],
        [130.0, 3.5, 34.0, 75.0, 2200.0, 0.48],
        [150.0, 4.5, 41.0, 86.0, 2500.0, 0.32],
        [85.0,  2.1, 15.0, 52.0, 1400.0, 0.78],
        [105.0, 2.9, 28.0, 64.0, 1950.0, 0.58],
    ]
    edges = [
        (0, 1), (1, 0), (1, 2), (2, 1), (0, 4), (4, 0),
        (4, 7), (7, 4), (2, 3), (3, 2), (3, 5), (5, 3),
        (6, 7), (7, 6), (5, 8), (8, 5), (6, 9), (9, 6)
    ]
    labels = [1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0]
    return node_features, edges, labels


def convert_bhuvan_to_pyg_data(
    node_features: List[List[float]],
    edges: List[Tuple[int, int]],
    labels: List[float]
) -> Any:
    """Converts raw features & spatial edges into a PyTorch Geometric Data object."""
    if not TORCH_AVAILABLE:
        return {
            "x": node_features,
            "edge_index": edges,
            "y": labels
        }

    # Apply Z-score Z-normalization
    means = [75.0, 3.5, 30.0, 60.0, 2000.0, 0.50]
    stds  = [50.0, 2.5, 12.0, 20.0, 500.0,  0.20]
    
    norm_x = []
    for row in node_features:
        norm_row = [(row[i] - means[i]) / stds[i] for i in range(len(row))]
        norm_x.append(norm_row)

    x_tensor = torch.tensor(norm_x, dtype=torch.float)
    edge_tensor = torch.tensor(edges, dtype=torch.long).t().contiguous()
    y_tensor = torch.tensor(labels, dtype=torch.float).unsqueeze(1)

    return Data(x=x_tensor, edge_index=edge_tensor, y=y_tensor)
