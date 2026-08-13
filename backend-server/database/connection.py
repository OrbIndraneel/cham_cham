"""
[DATABASE CONNECTION ENGINE] Provides database session management with fallback support.
"""
from typing import Generator
import logging
from database.db_config import DATABASE_URL, USE_MOCK_FALLBACK

logger = logging.getLogger("disaster_db")

_engine = None
_session_factory = None

def get_engine():
    global _engine
    if _engine is None:
        try:
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker
            
            _engine = create_engine(
                DATABASE_URL,
                pool_pre_ping=True,
                connect_args={"connect_timeout": 3}
            )
            # Test connection
            with _engine.connect() as conn:
                pass
            logger.info("Successfully connected to PostgreSQL + PostGIS database.")
        except Exception as e:
            logger.warning(f"PostgreSQL connection failed: {e}")
            if not USE_MOCK_FALLBACK:
                raise e
            _engine = False  # Mark fallback active
    return _engine

def get_db() -> Generator:
    """FastAPI Dependency yield for database sessions."""
    engine = get_engine()
    if engine and engine is not False:
        from sqlalchemy.orm import sessionmaker
        session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = session_factory()
        try:
            yield db
        finally:
            db.close()
    else:
        # Fallback generator yielding None (Repositories handle fallback logic)
        yield None
