import uuid
import asyncio
from queue import Queue, Empty
from loguru import logger
from scheduler.scheduler_service import get_scheduler

class MessageAdapter:
    """
    消息适配器
    负责将消息处理任务提交给调度器
    """
    def __init__(self):
        self.scheduler = get_scheduler()
        self.queue = Queue()
        self.running = False

    async def process_message_job(self, sender: str, content: str, config: dict):
        """
        处理消息的任务函数 (JOB)
        这里是实际的业务逻辑处理
        """
        logger.info(f"[JOB START] Processing message from {sender}: {content}")
        
        # TODO: 根据 config 执行具体的回复逻辑
        # 例如：调用 LLM 生成回复，或查找预设回复
        
        # 模拟处理耗时
        # await asyncio.sleep(1)
        
        logger.info(f"[JOB END] Finished processing message from {sender}")

    def add_job(self, sender: str, content: str, config: dict):
        """
        将消息处理任务放入队列，等待后台 worker 提交给调度器
        """
        try:
            self.queue.put((sender, content, config))
            logger.debug(f"Queued job for {sender}")
        except Exception as e:
            logger.error(f"Failed to queue job for {sender}: {e}")

    async def start_worker(self):
        """
        启动后台工作协程，从队列中取出任务并提交给调度器
        """
        self.running = True
        logger.info("MessageAdapter worker started.")
        while self.running:
            try:
                # 非阻塞获取，或者使用 asyncio.sleep 避免阻塞事件循环
                # 由于 queue.get 是阻塞的，我们需要在 executor 中运行，或者使用 asyncio.Queue
                # 但是 add_job 是从同步线程调用的，asyncio.Queue 不是线程安全的（虽然 call_soon_threadsafe 可以）
                # 最简单的方法：使用同步 Queue，这里用非阻塞 get + sleep
                try:
                    sender, content, config = self.queue.get_nowait()
                    
                    job_id = f"msg_process_{sender}_{uuid.uuid4()}"
                    logger.info(f"Submitting job {job_id} to scheduler")
                    
                    # 提交一次性任务
                    await self.scheduler.add_schedule(
                        self.process_message_job,
                        args=[sender, content, config],
                        id=job_id
                    )
                    
                except Empty:
                    await asyncio.sleep(0.5)
                    
            except Exception as e:
                logger.error(f"Error in MessageAdapter worker: {e}")
                await asyncio.sleep(1)

    def stop_worker(self):
        self.running = False

message_adapter = MessageAdapter()
