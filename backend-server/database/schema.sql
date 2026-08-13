-- Enable PostGIS spatial extension
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Relief Shelters Table
CREATE TABLE IF NOT EXISTS shelters (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location GEOMETRY(Point, 4326) NOT NULL,
    capacity INT NOT NULL,
    current_occupancy INT NOT NULL DEFAULT 0,
    status VARCHAR(50) NOT NULL DEFAULT 'Open',
    address TEXT,
    contact VARCHAR(100),
    medical_facilities_available BOOLEAN DEFAULT TRUE,
    food_supplies_days INT DEFAULT 7,
    power_generator BOOLEAN DEFAULT TRUE,
    helipad_access BOOLEAN DEFAULT FALSE,
    water_supply_liters INT DEFAULT 5000,
    admin_incharge_name VARCHAR(150),
    admin_incharge_phone VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Spatial GIST Index for high-speed radius/distance queries
CREATE INDEX IF NOT EXISTS idx_shelters_location ON shelters USING GIST (location);

-- 2. Hazard Cascade Risk Polygons Table
CREATE TABLE IF NOT EXISTS hazard_zones (
    id SERIAL PRIMARY KEY,
    district_id VARCHAR(50) NOT NULL,
    primary_hazard VARCHAR(100) NOT NULL,
    secondary_cascade_hazard VARCHAR(100) NOT NULL,
    cascade_probability FLOAT NOT NULL,
    estimated_lead_time_mins INT NOT NULL,
    risk_level VARCHAR(20) NOT NULL, -- 'High', 'Medium', 'Low'
    affected_population_estimate INT DEFAULT 0,
    severity_score FLOAT DEFAULT 5.0,
    soil_saturation_index FLOAT DEFAULT 0.0,
    elevation_m FLOAT DEFAULT 0.0,
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP WITH TIME ZONE,
    geometry GEOMETRY(Polygon, 4326) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Spatial GIST Index for ST_Contains hazard zone queries
CREATE INDEX IF NOT EXISTS idx_hazard_geometry ON hazard_zones USING GIST (geometry);

-- 3. Live Weather & River Sensor Readings Table
CREATE TABLE IF NOT EXISTS weather_readings (
    id SERIAL PRIMARY KEY,
    station_id VARCHAR(50) NOT NULL,
    station_name VARCHAR(150),
    rainfall_mm FLOAT NOT NULL DEFAULT 0.0,
    river_level_m FLOAT,
    humidity_pct FLOAT DEFAULT 0.0,
    wind_speed_kmh FLOAT DEFAULT 0.0,
    soil_moisture_pct FLOAT DEFAULT 0.0,
    temp_celsius FLOAT DEFAULT 0.0,
    alert_triggered BOOLEAN DEFAULT FALSE,
    location GEOMETRY(Point, 4326),
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Calculated Evacuation Routes Table
CREATE TABLE IF NOT EXISTS evacuation_routes (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(100),
    user_origin GEOMETRY(Point, 4326) NOT NULL,
    destination_shelter_id VARCHAR(50) REFERENCES shelters(id),
    route_path GEOMETRY(LineString, 4326) NOT NULL,
    distance_km FLOAT NOT NULL,
    estimated_time_mins INT NOT NULL,
    transport_mode VARCHAR(50) DEFAULT 'walking',
    waypoints_json JSONB,
    hazard_penalty_score FLOAT DEFAULT 1.0,
    hazard_avoided BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Emergency SOS Alerts Table
CREATE TABLE IF NOT EXISTS sos_alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(100) NOT NULL,
    user_name VARCHAR(150),
    user_phone VARCHAR(50),
    location GEOMETRY(Point, 4326) NOT NULL,
    emergency_type VARCHAR(100) NOT NULL, -- 'Trapped', 'Medical', 'Food/Water', 'Rescue Needed'
    status VARCHAR(50) DEFAULT 'Pending',   -- 'Pending', 'Dispatched', 'Rescued', 'Resolved'
    assigned_rescue_team_id VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_sos_location ON sos_alerts USING GIST (location);

-- 6. OpenStreetMap Road Network Edges Table
CREATE TABLE IF NOT EXISTS road_network_edges (
    id SERIAL PRIMARY KEY,
    source_node INT NOT NULL,
    target_node INT NOT NULL,
    length_m FLOAT NOT NULL,
    geom GEOMETRY(LineString, 4326) NOT NULL,
    hazard_penalty FLOAT DEFAULT 1.0,
    is_blocked BOOLEAN DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_road_geom ON road_network_edges USING GIST (geom);

-- 7. Disaster Incident History Table
CREATE TABLE IF NOT EXISTS incident_history (
    id SERIAL PRIMARY KEY,
    disaster_type VARCHAR(100) NOT NULL,
    district_id VARCHAR(50) NOT NULL,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE,
    total_casualties INT DEFAULT 0,
    damage_estimate_inr NUMERIC(15, 2),
    summary TEXT
);
