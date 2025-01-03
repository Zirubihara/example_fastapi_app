from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine

from api.health_routes import router as health_router
from api.odd_numbers_routes import router as odd_numbers_router
from api.user_routes import router as user_router  # Import the user router
from config import Config
from database import \
    Base  # Ensure you have the correct path to the database file
from logger import logger  # Import logger
from middleware import add_cors_middleware
from schemas.odd_numbers_reponse_model import \
    OddNumbersResponse  # Updated import for Pydantic model
from timing_decorator import time_logger  # Import timing decorator

# Create engine using the configuration
engine = create_engine(Config.DATABASE_URL)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
add_cors_middleware(app)

# Include the user router
app.include_router(user_router)
app.include_router(health_router)
app.include_router(odd_numbers_router)
