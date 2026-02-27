import os
from apscheduler import AsyncScheduler
from apscheduler.datastores.sqlalchemy import SQLAlchemyDataStore
from sqlalchemy.ext.asyncio import create_async_engine
from loguru import logger

# Get the directory of this file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the project root directory (3 levels up from src/backend/scheduler)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_DIR)))

# Define the database path
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, 'scheduler.db')
logger.info(f"Scheduler DB Path: {DB_PATH}")

# Ensure the directory for the DB exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Async Engine for SQLite (requires aiosqlite)
# Note: We use sqlite+aiosqlite for async support
engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}")

# DataStore
data_store = SQLAlchemyDataStore(engine)

# Create the scheduler instance
# We use AsyncScheduler for better integration with FastAPI
scheduler = AsyncScheduler(data_store)

def get_scheduler():
    """Get the scheduler instance."""
    return scheduler
