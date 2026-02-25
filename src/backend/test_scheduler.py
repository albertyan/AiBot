import sys
import os
import time

# Add src/backend to path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CURRENT_DIR)

from scheduler import start_scheduler, shutdown_scheduler, get_scheduler
from scheduler.scheduler_service import DB_PATH

def test_job():
    print("Test job executed!")

def main():
    print(f"Testing scheduler with DB: {DB_PATH}")
    
    start_scheduler()
    scheduler = get_scheduler()
    
    # Add a job
    job = scheduler.add_job(test_job, 'interval', seconds=2, id='test_job', replace_existing=True)
    print(f"Added job: {job}")
    
    # Wait for execution
    print("Waiting for job execution...")
    time.sleep(5)
    
    # Check if DB exists
    if os.path.exists(DB_PATH):
        print(f"DB created successfully at {DB_PATH}")
    else:
        print(f"Error: DB not found at {DB_PATH}")
        
    shutdown_scheduler()
    print("Test completed.")

if __name__ == "__main__":
    main()
