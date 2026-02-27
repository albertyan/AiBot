import asyncio
import os
import sys
import logging
from apscheduler import ConflictPolicy

# Configure logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

# Ensure src/backend is in path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CURRENT_DIR)

from scheduler import scheduler
from apscheduler.triggers.interval import IntervalTrigger
from test_job_module import test_job

async def main():
    print("Starting scheduler test (v4)...")
    
    # Use the scheduler as a context manager
    async with scheduler:
        # Important: Start the scheduler loop in background
        await scheduler.start_in_background()
        print("Scheduler started in background.")

        # Add a schedule
        print("Adding schedule...")
        try:
            # We use conflict_policy=ConflictPolicy.replace to ensure update if exists
            await scheduler.add_schedule(test_job, IntervalTrigger(seconds=1), id='test_job_v4', conflict_policy=ConflictPolicy.replace)
            print("Job added.")
        except Exception as e:
            print(f"Error adding schedule: {e}")
        
        print("Waiting for execution (5 seconds)...")
        await asyncio.sleep(5)
        
    print("Scheduler stopped.")

# if __name__ == "__main__":
#     if sys.platform == 'win32':
#         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     asyncio.run(main())
