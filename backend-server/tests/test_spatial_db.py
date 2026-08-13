from database.repositories import (
    haversine_distance,
    point_in_polygon,
    SpatialShelterRepository,
    SpatialHazardRepository
)
from data_pipeline.ingestion import SensorDataIngestionPipeline

def test_haversine_distance():
    # Shimla (31.1048, 77.1734) to Solan (30.9045, 77.0967) is ~23 km
    dist = haversine_distance(31.1048, 77.1734, 30.9045, 77.0967)
    assert 20.0 <= dist <= 26.0

def test_point_in_polygon_inside():
    polygon = [
        [31.0, 77.0],
        [31.0, 78.0],
        [32.0, 78.0],
        [32.0, 77.0]
    ]
    assert point_in_polygon(31.5, 77.5, polygon) is True

def test_point_in_polygon_outside():
    polygon = [
        [31.0, 77.0],
        [31.0, 78.0],
        [32.0, 78.0],
        [32.0, 77.0]
    ]
    assert point_in_polygon(30.0, 77.5, polygon) is False

def test_spatial_shelter_repository():
    repo = SpatialShelterRepository(db_session=None)
    shelters = repo.get_nearby_shelters(31.1048, 77.1734, radius_km=20.0)
    assert len(shelters) > 0
    # Output should be sorted by distance
    for i in range(len(shelters) - 1):
        assert shelters[i]["distance_km"] <= shelters[i + 1]["distance_km"]

def test_sensor_ingestion_pipeline():
    pipeline = SensorDataIngestionPipeline(db_session=None)
    readings = pipeline.fetch_live_sensor_readings()
    assert len(readings) == 2
    triggers = pipeline.evaluate_cascade_trigger_conditions(readings)
    assert len(triggers) > 0
    assert triggers[0]["trigger_type"] == "Compound_Hydrological_Risk"
