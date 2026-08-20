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
