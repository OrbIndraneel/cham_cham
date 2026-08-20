import pytest
from optimization.route_optimizer import EvacuationRouteOptimizer, is_point_in_polygon

def test_point_in_polygon():
    # Square polygon around (31.11, 77.18)
    polygon = [
        [31.10, 77.17],
        [31.12, 77.17],
        [31.12, 77.19],
        [31.10, 77.19]
    ]
    assert is_point_in_polygon(31.11, 77.18, polygon) is True
    assert is_point_in_polygon(31.25, 77.50, polygon) is False

def test_evacuation_route_optimizer_basic():
    optimizer = EvacuationRouteOptimizer()
    origin_lat, origin_lng = 31.1048, 77.1754
    target_lat, target_lng = 31.1248, 77.2004

    result = optimizer.calculate_evacuation_route(origin_lat, origin_lng, target_lat, target_lng)

    assert "distance_km" in result
    assert result["distance_km"] > 0
    assert result["estimated_time_mins"] > 0
    assert len(result["route_coordinates"]) >= 3
    assert result["route_coordinates"][0] == [origin_lat, origin_lng]
    assert result["route_coordinates"][-1] == [target_lat, target_lng]

def test_evacuation_route_optimizer_hazard_reroute():
    optimizer = EvacuationRouteOptimizer()
    origin_lat, origin_lng = 31.1048, 77.1754
    target_lat, target_lng = 31.1248, 77.2004

    mid_lat = (origin_lat + target_lat) / 2.0
    mid_lng = (origin_lng + target_lng) / 2.0

    # Create a hazard polygon surrounding the direct midpoint node
    hazard_polygon = [
        [round(mid_lat - 0.003, 4), round(mid_lng - 0.003, 4)],
        [round(mid_lat + 0.003, 4), round(mid_lng - 0.003, 4)],
        [round(mid_lat + 0.003, 4), round(mid_lng + 0.003, 4)],
        [round(mid_lat - 0.003, 4), round(mid_lng + 0.003, 4)]
    ]

    result = optimizer.calculate_evacuation_route(
        origin_lat, origin_lng, target_lat, target_lng, hazard_polygons=[hazard_polygon]
    )

    assert result["distance_km"] > 0
    # The route should reroute via North or South mid node instead of direct_mid
    direct_mid_coord = [round(mid_lat, 4), round(mid_lng, 4)]
    assert direct_mid_coord not in result["route_coordinates"]
