import math
from typing import List, Dict, Any, Tuple, Optional
try:
    import networkx as nx
except ImportError:
    nx = None

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates distance between two coordinates in kilometers."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 3)

def is_point_in_polygon(lat: float, lng: float, polygon: List[List[float]]) -> bool:
    """Ray-casting algorithm to evaluate if (lat, lng) falls inside polygon."""
    if not polygon or len(polygon) < 3:
        return False
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if lat > min(p1x, p2x):
            if lat <= max(p1x, p2x):
                if lng <= max(p1y, p2y):
                    if p1x != p2x:
                        xinters = (lat - p1x) * (p2y - p1y) / (p2x - p1x) + p1y
                    if p1y == p2y or lng <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

class EvacuationRouteOptimizer:
    """
    [OPTIMIZATION ENGINE] Evacuation Route Optimization Engine using NetworkX graph pathfinding.
    Calculates shortest and safest paths by assigning high penalties to GNN-flagged hazard edges.
    """
    def __init__(self, road_network_graph=None):
        if road_network_graph is not None:
            self.graph = road_network_graph
        elif nx is not None:
            self.graph = nx.DiGraph()
        else:
            self.graph = None

    def build_sample_road_network(self, origin_lat: float, origin_lng: float, target_lat: float, target_lng: float):
        """
        Constructs a multi-path road network graph between origin and destination coordinates.
        Creates 3 main corridors: Direct, North Detour, South Detour.
        """
        if nx is None:
            return

        self.graph = nx.DiGraph()
        
        # Calculate midpoints for alternative corridors
        mid_lat = (origin_lat + target_lat) / 2.0
        mid_lng = (origin_lng + target_lng) / 2.0
        
        # Corridor nodes
        nodes = {
            "origin": (origin_lat, origin_lng),
            "direct_mid": (round(mid_lat, 4), round(mid_lng, 4)),
            "north_mid": (round(mid_lat + 0.008, 4), round(mid_lng + 0.004, 4)),
            "south_mid": (round(mid_lat - 0.008, 4), round(mid_lng - 0.004, 4)),
            "destination": (target_lat, target_lng)
        }

        for node_id, pos in nodes.items():
            self.graph.add_node(node_id, pos=pos, lat=pos[0], lng=pos[1])

        # Add directed road edges
        edges = [
            ("origin", "direct_mid"),
            ("direct_mid", "destination"),
            ("origin", "north_mid"),
            ("north_mid", "destination"),
            ("origin", "south_mid"),
            ("south_mid", "destination"),
        ]

        for u, v in edges:
            pos_u = self.graph.nodes[u]["pos"]
            pos_v = self.graph.nodes[v]["pos"]
            dist_km = haversine_km(pos_u[0], pos_u[1], pos_v[0], pos_v[1])
            dist_m = dist_km * 1000.0
            self.graph.add_edge(u, v, length_m=dist_m, dist_km=dist_km, hazard_penalty=1.0, weight=dist_m)

    def apply_hazard_penalties(self, high_risk_polygons: List[List[List[float]]], penalty_multiplier: float = 100.0) -> List[str]:
        """Increase edge weights for roads passing through predicted cascade zones."""
        if self.graph is None or not high_risk_polygons:
            return []

        penalized_nodes = []
        for node_id, data in self.graph.nodes(data=True):
            lat, lng = data.get("lat"), data.get("lng")
            if lat is None or lng is None:
                continue
            
            for poly in high_risk_polygons:
                if is_point_in_polygon(lat, lng, poly):
                    penalized_nodes.append(node_id)
                    break

        # Penalize edges connected to or passing through hazard nodes
        for u, v, data in self.graph.edges(data=True):
            if u in penalized_nodes or v in penalized_nodes:
                data["hazard_penalty"] = penalty_multiplier
                data["weight"] = data["length_m"] * penalty_multiplier

        return penalized_nodes

    def compute_shortest_safe_path(self, origin: str = "origin", destination: str = "destination") -> Tuple[List[str], float, bool]:
        """Computes path avoiding hazard-penalized roads using Dijkstra algorithm."""
        if self.graph is None or not self.graph.has_node(origin) or not self.graph.has_node(destination):
            return [origin, destination], 0.0, False

        try:
            path_nodes = nx.dijkstra_path(self.graph, origin, destination, weight="weight")
            
            # Calculate actual geographic distance
            total_dist_km = 0.0
            hazard_avoided = True
            for i in range(len(path_nodes) - 1):
                u, v = path_nodes[i], path_nodes[i+1]
                edge_data = self.graph[u][v]
                total_dist_km += edge_data.get("dist_km", 0.0)
                if edge_data.get("hazard_penalty", 1.0) > 1.0:
                    hazard_avoided = False

            return path_nodes, round(total_dist_km, 2), hazard_avoided
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return [origin, destination], 0.0, False

    def calculate_evacuation_route(
        self,
        origin_lat: float,
        origin_lng: float,
        target_lat: float,
        target_lng: float,
        hazard_polygons: Optional[List[List[List[float]]]] = None
    ) -> Dict[str, Any]:
        """
        High-level route calculation entry point. Builds road graph, applies hazard penalties,
        and returns waypoints & metadata.
        """
        self.build_sample_road_network(origin_lat, origin_lng, target_lat, target_lng)

        if hazard_polygons:
            self.apply_hazard_penalties(hazard_polygons)

        path_nodes, dist_km, hazard_avoided = self.compute_shortest_safe_path("origin", "destination")

        route_waypoints = [
            [self.graph.nodes[nid]["lat"], self.graph.nodes[nid]["lng"]]
            for nid in path_nodes
        ]

        if dist_km == 0.0:
            dist_km = haversine_km(origin_lat, origin_lng, target_lat, target_lng)

        est_time_mins = max(5, int(dist_km * 4.5))

        return {
            "distance_km": dist_km,
            "estimated_time_mins": est_time_mins,
            "hazard_avoided": hazard_avoided,
            "route_coordinates": route_waypoints
        }

