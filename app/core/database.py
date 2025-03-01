# database.py

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import QueuePool

from config import Config
from logger import logger


class Base(DeclarativeBase):
    pass


def create_database_engine():
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

        # Test connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            connection.commit()
            logger.info("Database connection established successfully")

        return engine

    except Exception as e:
        logger.error(f"Failed to create database engine: {str(e)}")
        raise


engine = create_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
