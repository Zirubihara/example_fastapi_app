from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import QueuePool

from config import Config
from logger import logger


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    pass


def create_database_engine() -> Engine:
    """
    Create and configure the SQLAlchemy engine.

    Returns:
        Engine: Configured SQLAlchemy engine

    Raises:
        Exception: If database connection cannot be established
    """
    try:
        engine = create_engine(
            Config.DATABASE_URL,
            poolclass=QueuePool,
            pool_size=Config.DATABASE_POOL_SIZE,
            max_overflow=Config.DATABASE_MAX_OVERFLOW,
            pool_timeout=30,  # seconds
            pool_pre_ping=True,  # enable connection health checks
            echo=Config.DEBUG,  # log SQL queries in debug mode
        )

        # Verify database connection
        with engine.connect() as connection:
            connection.execute("SELECT 1")
            logger.info("Database connection established successfully")

        return engine

    except Exception as e:
        logger.error(f"Failed to create database engine: {str(e)}")
        raise


def get_db() -> Generator:
    """
    Get database session generator.

    Yields:
        Session: Database session
    """
    engine = create_database_engine()
    SessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
    )

    db = SessionLocal()
    try:
        yield db
        logger.debug("Database session created successfully")
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        raise
    finally:
        db.close()
        logger.debug("Database session closed")


# Create database engine
engine = create_database_engine()

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)

# Initialize Base for models
Base = Base()
