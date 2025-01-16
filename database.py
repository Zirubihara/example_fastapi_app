from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import QueuePool
from config import Config
from logger import logger
from typing import Generator


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    pass


def create_database_engine():
    """
    Create and configure the SQLAlchemy engine.

    Returns:
        Engine: Configured SQLAlchemy engine
    """
    try:
        engine = create_engine(
            Config.DATABASE_URL,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_pre_ping=True,
            echo=Config.DEBUG,
        )

        # Verify database connection
        with engine.connect() as connection:
            connection.execute(
                text("SELECT 1")
            )  # Użyj text() do utworzenia wykonywalnego SQL
            connection.commit()
            logger.info("Database connection established successfully")

        return engine

    except Exception as e:
        logger.error(f"Failed to create database engine: {str(e)}")
        raise


def get_db() -> Generator:
    """Database session generator."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create database engine
engine = create_database_engine()

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize Base
Base = Base()
