import logging
logger = logging.getLogger(__name__)

async def test_job():
    print("PRINT: Test job executed from module!")
    logger.info("LOG: Test job executed from module!")
