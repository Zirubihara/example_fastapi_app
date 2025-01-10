from fastapi import FastAPI
from sqlalchemy import create_engine

from api.health_routes import router as health_router
from api.odd_numbers_routes import router as odd_numbers_router
from api.user_routes import router as user_router
from config import Config
from database import Base
from logger import logger
from middleware import add_cors_middleware

app = FastAPI()

try:
    logger.info("Initializing database connection...")
    engine = create_engine(Config.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Database initialization failed: {e}")
    raise

logger.info("Adding CORS middleware")
add_cors_middleware(app)

logger.info("Including routers")
app.include_router(user_router, prefix="/users")
app.include_router(health_router, prefix="/health")
app.include_router(odd_numbers_router, prefix="/odd-numbers")

logger.info("Application startup complete")
