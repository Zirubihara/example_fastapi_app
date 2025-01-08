from fastapi import FastAPI
from sqlalchemy import create_engine

from api.health_routes import router as health_router
from api.odd_numbers_routes import router as odd_numbers_router
from api.user_routes import router as user_router
from config import Config
from database import Base
from middleware import add_cors_middleware

# Create engine using the configuration
engine = create_engine(Config.DATABASE_URL)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
add_cors_middleware(app)

# Include routers
app.include_router(user_router)
app.include_router(health_router)
app.include_router(odd_numbers_router)
