"""
[DATABASE LAYER] PostgreSQL + PostGIS Spatial Database Configuration.
"""
import os
from dotenv import load_dotenv

# Load .env file from project root or current directory if present
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "disaster_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Set to True to allow in-memory spatial fallback when PostgreSQL connection is unavailable
USE_MOCK_FALLBACK = os.getenv("USE_MOCK_FALLBACK", "true").lower() in ("true", "1", "yes")

