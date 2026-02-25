import os
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from loguru import logger

# Get the directory of this file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the project root directory (3 levels up from src/backend/scheduler)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_DIR)))

# Define the database path
DB_PATH = os.path.join(PROJECT_ROOT, 'scheduler.db')
logger.info(f"Scheduler DB Path: {DB_PATH}")

# Ensure the directory for the DB exists (just in case, though root usually exists)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Configuration for APScheduler
jobstores = {
    'default': SQLAlchemyJobStore(url=f'sqlite:///{DB_PATH}')
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

# Create the scheduler instance
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone='Asia/Shanghai')

def start_scheduler():
    """Start the scheduler if it's not already running."""
    if not scheduler.running:
        try:
            scheduler.start()
            logger.info("APScheduler started successfully.")
        except Exception as e:
            logger.error(f"Failed to start APScheduler: {e}")

def shutdown_scheduler():
    """Shutdown the scheduler."""
    if scheduler.running:
        try:
            scheduler.shutdown()
            logger.info("APScheduler shutdown successfully.")
        except Exception as e:
            logger.error(f"Failed to shutdown APScheduler: {e}")

def get_scheduler():
    """Get the scheduler instance."""
    return scheduler
