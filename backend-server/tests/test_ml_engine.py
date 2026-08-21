from ml_engine.models.gat_cascade import GATCascadeNet
from ml_engine.feature_engineering.graph_builder import SpatialGraphBuilder
from ml_engine.inference import CascadePredictor

def test_spatial_graph_builder():
    builder = SpatialGraphBuilder()
    graph_data = builder.build_spatial_grid_graph(31.1048, 77.1734, rainfall_mm=120.0, river_level_m=5.0)
    assert graph_data is not None

def test_gat_cascade_net_initialization():
    model = GATCascadeNet(in_channels=6)
    assert model is not None

def test_cascade_predictor_inference():
    predictor = CascadePredictor()
    result = predictor.predict_cascade_hazard(
        latitude=31.1048,
        longitude=77.1734,
        rainfall_mm=135.0,
        river_level_m=9.2,
        district_id="DIST_SHIMLA_HIGH"
    )
    assert result["district_id"] == "DIST_SHIMLA_HIGH"
    assert result["risk_level"] in ("High", "Medium", "Low")
    assert 0.0 <= result["cascade_probability"] <= 1.0
    assert 15 <= result["estimated_lead_time_mins"] <= 180
    assert len(result["polygon_coordinates"]) == 4

def test_combined_disaster_engine():
    from ml_engine.combined_disaster_engine import CombinedDisasterEngine
    engine = CombinedDisasterEngine()
    result = engine.predict({
        "latitude": 30.73,
        "longitude": 79.06,
        "district_id": "CHAMOLI_01",
        "Rainfall_mm": 380.0,
        "Water_Level_m": 8.5,
        "Elevation_m": 2200,
        "slope_angle_deg": 44.0
    })
    assert "stage_1_local_flood_risk" in result
    assert "stage_2_spatial_cascade_hazard" in result
    assert "unified_disaster_assessment" in result
    assert 0.0 <= result["unified_disaster_assessment"]["unified_risk_score"] <= 1.0
