import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend-server')))

from database.connection import get_engine
from sqlalchemy import text

def setup_supabase_schema():
    print("=== INITIALIZING SUPABASE POSTGRESQL + POSTGIS DATABASE SCHEMA ===")
    engine = get_engine()
    if not engine or engine is False:
        print("Error: Unable to connect to Supabase database. Please check DATABASE_URL in backend-server/.env.")
        return

    with engine.connect() as conn:
        # Enable PostGIS extension
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
        
        # 1. Create Shelters Table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS shelters (
                id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                capacity INT NOT NULL DEFAULT 500,
                current_occupancy INT NOT NULL DEFAULT 0,
                status VARCHAR(50) NOT NULL DEFAULT 'Open',
                address TEXT,
                contact VARCHAR(50),
                medical_facilities_available BOOLEAN DEFAULT TRUE,
                food_supplies_days INT DEFAULT 7,
                power_generator BOOLEAN DEFAULT TRUE,
                helipad_access BOOLEAN DEFAULT FALSE,
                water_supply_liters INT DEFAULT 5000,
                admin_incharge_name VARCHAR(100),
                admin_incharge_phone VARCHAR(50),
                location GEOMETRY(Point, 4326)
            );
        """))

        # 2. Create Hazard Zones Table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS hazard_zones (
                id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                hazard_type VARCHAR(50) NOT NULL,
                severity VARCHAR(50) NOT NULL,
                probability FLOAT DEFAULT 0.85,
                affected_population INT DEFAULT 45000,
                is_active BOOLEAN DEFAULT TRUE,
                geometry GEOMETRY(Polygon, 4326)
            );
        """))

        # 3. Create Emergency SOS Alerts Table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS sos_alerts (
                id VARCHAR(50) PRIMARY KEY,
                user_id VARCHAR(100) NOT NULL,
                user_name VARCHAR(100),
                user_phone VARCHAR(50),
                emergency_type VARCHAR(100) NOT NULL,
                status VARCHAR(50) NOT NULL DEFAULT 'Pending',
                notes TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                location GEOMETRY(Point, 4326)
            );
        """))

        # 4. Create Emergency Broadcast Alerts Table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS broadcast_alerts (
                id VARCHAR(50) PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                body TEXT NOT NULL,
                severity VARCHAR(50) NOT NULL,
                disaster_type VARCHAR(50) NOT NULL,
                target_region VARCHAR(100) NOT NULL,
                issued_by VARCHAR(100) DEFAULT 'Authority Command & Control Center',
                issued_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                action_required VARCHAR(100) NOT NULL,
                affected_population_estimate INT DEFAULT 42500,
                acknowledgment_required BOOLEAN DEFAULT FALSE
            );
        """))
        
        # Seed initial real shelter data if table is empty
        res = conn.execute(text("SELECT COUNT(*) FROM shelters;")).scalar()
        if res == 0:
            conn.execute(text("""
                INSERT INTO shelters (id, name, capacity, current_occupancy, status, address, contact, location)
                VALUES 
                ('sh_vad_01', 'Akota Indoor Sports Stadium Relief Camp', 1200, 340, 'Open', 'Akota, Vadodara, Gujarat', '+91-265-2331001', ST_SetSRID(ST_MakePoint(73.1812, 22.3072), 4326)),
                ('sh_vad_02', 'Sayajigunj Community Center Emergency Shelter', 800, 150, 'Open', 'Sayajigunj, Vadodara, Gujarat', '+91-265-2331002', ST_SetSRID(ST_MakePoint(73.1880, 22.3120), 4326)),
                ('sh_vad_03', 'Fatehgunj Relief & Medical Operations Center', 650, 80, 'Open', 'Fatehgunj, Vadodara, Gujarat', '+91-265-2331003', ST_SetSRID(ST_MakePoint(73.1920, 22.3200), 4326));
            """))
            print("[SUCCESS] Seeded initial relief shelter records into Supabase PostGIS table.")

        conn.commit()
        print("[SUCCESS] Supabase PostgreSQL + PostGIS Schema initialized successfully!")

if __name__ == '__main__':
    setup_supabase_schema()
