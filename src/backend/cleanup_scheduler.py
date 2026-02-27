import asyncio
import os
import sys
import logging
from apscheduler import AsyncScheduler
from apscheduler.datastores.sqlalchemy import SQLAlchemyDataStore
from sqlalchemy.ext.asyncio import create_async_engine

# Configure logging
logging.basicConfig(level=logging.INFO)

# Setup paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# H:\traeworkspace\AiBot\src\backend -> H:\traeworkspace\AiBot
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
DB_PATH = os.path.join(DATA_DIR, 'scheduler.db')

async def main():
    print(f"Connecting to DB: {DB_PATH}")
    if not os.path.exists(DB_PATH):
        print("DB does not exist.")
        return

    engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}")
    data_store = SQLAlchemyDataStore(engine)
    scheduler = AsyncScheduler(data_store)
    
    async with scheduler:
        await scheduler.start_in_background()
        schedules = await scheduler.get_schedules()
        print(f"Found {len(schedules)} schedules:")
        for schedule in schedules:
            print(f" - ID: {schedule.id}, Task: {schedule.task_id}, Next run: {schedule.next_fire_time}")
            
            # Delete ALL test jobs
            if 'test_job' in schedule.id or 'test_job' in str(schedule.task_id):
                 print(f"   Deleting schedule {schedule.id}...")
                 await scheduler.remove_schedule(schedule.id)

    print("Cleanup complete.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
