# Software Requirements Specification (SRS)
## Disaster Management AI Platform
### Early Cascade Disaster Prediction & Dynamic Hazard-Avoiding Evacuation Route Optimization

**Document Version:** 1.0.0  
**Target Project:** Smart India Hackathon (SIH) 2026 Target Project  
**Date:** August 14, 2026  
**Status:** Approved Technical Base  

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) document specifies the complete functional, non-functional, interface, and architectural requirements for the **Disaster Management AI Platform**. The platform provides early predictions of secondary compound disaster cascades (*e.g., Heavy Rainfall $\rightarrow$ Landslide $\rightarrow$ Flash Flood*) and dynamically calculates safest, hazard-avoiding evacuation routes to relief camps.

### 1.2 Scope
The Disaster Management AI Platform is an end-to-end intelligent disaster response system designed to bridge the 12-hour response latency gap in traditional infrastructure. The system:
- Ingests live precipitation and river gauge telemetry from IMD (India Meteorological Department) and CWC (Central Water Commission).
- Employs a **PyTorch Geometric (PyG) Graph Attention Network (GAT)** to forecast compound cascade risks up to 60 minutes in advance.
- Uses **PostgreSQL + PostGIS** spatial indexing (GIST R-Tree) for point-in-polygon hazard geofencing (`ST_Contains`) and nearest shelter lookups (`ST_DWithin`).
- Uses **Google OR-Tools & NetworkX** graph pathfinding to calculate safest evacuation routes that avoid GNN-flagged risk zones.
- Provides high-priority Emergency SOS alert dispatch for trapped citizens.

### 1.3 Definitions and Acronyms
- **SRS**: Software Requirements Specification
- **GNN**: Graph Neural Network
- **GAT**: Graph Attention Network
- **PostGIS**: Spatial Database Extension for PostgreSQL
- **OR-Tools**: Google Operations Research Optimization Suite
- **IMD**: India Meteorological Department
- **CWC**: Central Water Commission
- **SOS**: Save Our Souls (Emergency Distress Signal)
- **REST**: Representational State Transfer API

---

## 2. Overall Description

### 2.1 Product Perspective & 4 Core Pillars
The system operates as a 4-pillar modular software platform:

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                       1. LIVE DATA INGESTION PIPELINE                   │
 │  IMD Rainfall Sensors  ──>  CWC River Gauges  ──>  Threshold Triggers   │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │ Sensor Stream
 ┌────────────────────────────────────▼────────────────────────────────────┐
 │                       2. GNN CASCADE ML ENGINE                          │
 │  PyTorch Geometric GAT  ──>  Predicts Secondary Hazards & Lead Time     │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │ Risk Polygon & Probability
 ┌────────────────────────────────────▼────────────────────────────────────┐
 │                       3. SPATIAL DATABASE LAYER                         │
 │  PostgreSQL + PostGIS  ──>  GIST Index  ──>  ST_Contains / ST_DWithin   │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │ Spatial Boundaries & Shelters
 ┌────────────────────────────────────▼────────────────────────────────────┐
 │                  4. EVACUATION SOLVER & FASTAPI GATEWAY                 │
 │  Google OR-Tools / NetworkX  ──>  FastAPI  ──>  Hazard-Avoiding Routes  │
 └─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 User Classes & Characteristics
1. **General Public / Citizens**: Accesses hazard risk predictions, views safe evacuation route polylines, and broadcasts emergency SOS distress requests.
2. **Emergency Response Teams / Admins**: Monitors active SOS distress alerts, views affected population estimates, manages relief shelter capacities, and dispatches rescue personnel.
3. **Automated Weather System**: Ingests sensor streams from IMD and CWC stations into the database every minute.

### 2.3 Operating Environment
- **Backend OS**: Windows / Linux / macOS (Python 3.10+)
- **Database Engine**: PostgreSQL 15+ with PostGIS 3.3+ spatial extension (Local or Supabase Cloud)
- **API Framework**: FastAPI with Uvicorn ASGI server
- **ML Framework**: PyTorch 2.0+ & PyTorch Geometric 2.3+

---

## 3. System Features & Functional Requirements

### 3.1 Live Data Ingestion Pipeline (`data_pipeline/ingestion.py`)
- **REQ-1.1**: The system SHALL ingest real-time rainfall data (mm) and river level gauge readings (m).
- **REQ-1.2**: The system SHALL trigger GNN ML evaluation when precipitation exceeds 100mm or river levels cross 8.0 meters.

### 3.2 GNN Cascade Prediction Model (`ml_engine/`)
- **REQ-2.1**: The system SHALL represent geographical regions as a Graph $G=(V, E)$ where nodes represent terrain units and edges represent topological/flow adjacencies.
- **REQ-2.2**: The Graph Attention Network (`GATConv`) SHALL compute dynamic attention coefficients ($\alpha_{ij}$) to forecast secondary cascade hazards.
- **REQ-2.3**: The model SHALL output `cascade_probability` (0.0 to 1.0), `estimated_lead_time_mins` (15 to 90 mins), `risk_level` ('High', 'Medium', 'Low'), and bounding `polygon_coordinates`.

### 3.3 Spatial Database & PostGIS Layer (`database/`)
- **REQ-3.1**: The system SHALL store spatial entities using WGS84 EPSG:4326 coordinate reference system.
- **REQ-3.2**: The database SHALL maintain spatial tables: `shelters` (Point), `hazard_zones` (Polygon), `weather_readings` (Point), `evacuation_routes` (LineString), `sos_alerts` (Point), `road_network_edges` (LineString), `incident_history`.
- **REQ-3.3**: The database SHALL index all spatial geometry columns using GIST (Generalized Search Tree) R-Tree indexes.
- **REQ-3.4**: The system SHALL support point-in-polygon hazard checking via `ST_Contains` and radius shelter lookup via `ST_DWithin` and `ST_DistanceSphere`.

### 3.4 Evacuation Route Optimizer (`optimization/route_optimizer.py`)
- **REQ-4.1**: The pathfinder SHALL assign penalty weight multipliers ($100\times$) to road edges passing through active GNN hazard polygons.
- **REQ-4.2**: The solver SHALL compute the shortest hazard-avoiding path between user origin and nearest available shelter.

### 3.5 Emergency SOS Alert System (`api/routes/sos_routes.py`)
- **REQ-5.1**: Citizens SHALL be able to submit emergency SOS rescue requests (`POST /api/sos`) with coordinates, emergency type ('Trapped', 'Medical', 'Food/Water', 'Rescue Needed'), and notes.
- **REQ-5.2**: Emergency response teams SHALL be able to retrieve active SOS alerts (`GET /api/sos/active`) filtered by spatial location.

---

## 4. Non-Functional Requirements

### 4.1 Performance Requirements
- **NFR-1.1 (Latency)**: API response time for `/api/predict-cascade` and `/api/evacuation-route` SHALL be less than 500 milliseconds under nominal load.
- **NFR-1.2 (Spatial Query Speed)**: PostGIS spatial queries (`ST_Contains`, `ST_DWithin`) SHALL execute in under 10 milliseconds using GIST R-Tree indexes.
- **NFR-1.3 (Target Impact)**: The platform SHALL target reducing disaster response latency from 12 hours to under 30 minutes, boosting casualty prevention up to 95%.

### 4.2 Reliability & Fault Tolerance
- **NFR-2.1 (Fallback Mode)**: If PostgreSQL/PostGIS is disconnected, the system SHALL automatically switch to built-in in-memory spatial fallback algorithms (Haversine & Ray-Casting) to maintain 100% uptime.

### 4.3 Security Requirements
- **NFR-3.1 (Input Sanitization)**: All inputs SHALL be validated using Pydantic schemas.
- **NFR-3.2 (Connection Security)**: Cloud database connections SHALL use SSL/TLS encryption (`sslmode=require`) and percent-encoded credential strings.

---

## 5. Appendix - Data Dictionary

| Table Name | Spatial Type | Core Attributes |
| :--- | :--- | :--- |
| `shelters` | Point(4326) | `id`, `name`, `location`, `capacity`, `current_occupancy`, `medical_facilities_available`, `food_supplies_days`, `power_generator`, `helipad_access`, `water_supply_liters` |
| `hazard_zones` | Polygon(4326) | `id`, `district_id`, `primary_hazard`, `secondary_cascade_hazard`, `cascade_probability`, `estimated_lead_time_mins`, `risk_level`, `affected_population_estimate`, `geometry` |
| `weather_readings` | Point(4326) | `id`, `station_id`, `rainfall_mm`, `river_level_m`, `humidity_pct`, `wind_speed_kmh`, `soil_moisture_pct`, `location`, `recorded_at` |
| `evacuation_routes` | LineString(4326) | `id`, `user_id`, `user_origin`, `destination_shelter_id`, `route_path`, `distance_km`, `estimated_time_mins`, `hazard_avoided` |
| `sos_alerts` | Point(4326) | `id`, `user_id`, `user_name`, `user_phone`, `location`, `emergency_type`, `status`, `notes`, `created_at` |
| `road_network_edges`| LineString(4326) | `id`, `source_node`, `target_node`, `length_m`, `geom`, `hazard_penalty`, `is_blocked` |
| `incident_history` | N/A | `id`, `disaster_type`, `district_id`, `start_time`, `end_time`, `total_casualties`, `damage_estimate_inr` |
