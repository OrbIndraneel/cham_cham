"""
[DATA INGESTION PIPELINE] Live rainfall & river gauge sensor ingestion service.
Ingests stream data from IMD (India Meteorological Department) & CWC (Central Water Commission).
"""
import time
from typing import Dict, Any, List
import logging

logger = logging.getLogger("data_ingestion")

# Sample IMD & CWC sensor stations across Himachal Pradesh & Uttarakhand risk zones
STATION_METADATA: List[Dict[str, Any]] = [
    {
        "station_id": "IMD_HP_001",
        "station_name": "Shimla Central Weather Observatory",
        "latitude": 31.1048,
        "longitude": 77.1734,
        "type": "rainfall"
    },
    {
        "station_id": "CWC_HP_102",
        "station_name": "Sutlej River Level Gauge - Rampur",
        "latitude": 31.4500,
        "longitude": 77.6300,
        "type": "river_gauge"
    },
    {
        "station_id": "IMD_UK_005",
        "station_name": "Chamoli Disaster Warning Station",
        "latitude": 30.4000,
        "longitude": 79.3300,
        "type": "rainfall"
    }
]

class SensorDataIngestionPipeline:
    def __init__(self, db_session=None):
        self.db = db_session

    def fetch_live_sensor_readings(self) -> List[Dict[str, Any]]:
        """Simulates/Fetches real-time sensor streams from IMD and CWC API gateways."""
        readings = [
            {
                "station_id": "IMD_HP_001",
                "station_name": "Shimla Central Weather Observatory",
                "rainfall_mm": 112.5,  # Heavy rainfall threshold > 100mm
                "river_level_m": 4.2,
                "latitude": 31.1048,
                "longitude": 77.1734,
                "timestamp": time.time(),
                "status": "Warning_Threshold_Exceeded"
            },
            {
                "station_id": "CWC_HP_102",
                "station_name": "Sutlej River Level Gauge - Rampur",
                "rainfall_mm": 85.0,
                "river_level_m": 8.7,  # Danger level > 8.0m
                "latitude": 31.4500,
                "longitude": 77.6300,
                "timestamp": time.time(),
                "status": "Danger_Level_Crossed"
            }
        ]
        logger.info(f"Ingested {len(readings)} live weather sensor readings.")
        return readings

    def evaluate_cascade_trigger_conditions(self, readings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identifies regions exceeding critical precipitation/water thresholds triggering ML GNN cascade evaluation."""
        triggered_zones = []
        for r in readings:
            if r["rainfall_mm"] >= 100.0 or (r["river_level_m"] and r["river_level_m"] >= 8.0):
                triggered_zones.append({
                    "district_id": r["station_id"],
                    "station_name": r["station_name"],
                    "latitude": r["latitude"],
                    "longitude": r["longitude"],
                    "rainfall_mm": r["rainfall_mm"],
                    "river_level_m": r["river_level_m"],
                    "trigger_type": "Compound_Hydrological_Risk"
                })
        return triggered_zones
