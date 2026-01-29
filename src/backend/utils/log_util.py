import os
import sys
import time
from pathlib import Path
from loguru import logger
import logging


# # 配置日志
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
class IgnoreWebSocketLogFilter(logging.Filter):
    """过滤掉 WebSocket 频繁连接/断开的日志"""
    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        if '"WebSocket /" [accepted]' in msg:
            return False
        if msg == "connection open" or msg == "connection closed":
            return False
        return True

# 将过滤器添加到 uvicorn 的 logger 中
for logger_name in ["uvicorn", "uvicorn.access", "uvicorn.error"]:
    logging.getLogger(logger_name).addFilter(IgnoreWebSocketLogFilter())

    
class LogConfig:
    """
    常用的 Loguru 配置类
    """
    
    # 日志存储路径
    LOG_PATH = Path(os.getcwd()) / "logs"
    
    # 日志格式
    # 简单的格式：时间 | 级别 | 模块:行号 - 消息
    FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    
    # 具体的日志文件配置
    ROTATION = "10 MB"  # 每个文件最大 10MB
    RETENTION = "7 days" # 保留最近 7 天的日志
    COMPRESSION = "zip"  # 压缩格式
    ENCODING = "utf-8"   # 编码格式

    def __init__(self, level: str = "INFO"):
        self.level = level
        self._ensure_log_dir()
        self._configure_logger()

    def _ensure_log_dir(self):
        """确保日志目录存在"""
        if not self.LOG_PATH.exists():
            self.LOG_PATH.mkdir(parents=True, exist_ok=True)

    def _configure_logger(self):
        """配置 logger"""
        # 移除默认的 handler (避免重复输出)
        logger.remove()

        # 1. 控制台输出 (Console)
        logger.add(
            sys.stderr,
            level=self.level,
            format=self.FORMAT,
            colorize=True,
            enqueue=True # 异步写入
        )

        # 2. 普通日志文件 (Info 及以上)
        # 每天一个文件: {time:YYYY-MM-DD}_info.log
        info_log_file = self.LOG_PATH / "{time:YYYY-MM-DD}_info.log"
        logger.add(
            str(info_log_file),
            level="INFO",
            format=self.FORMAT,
            rotation="00:00", # 每天午夜轮转
            retention=self.RETENTION,
            compression=self.COMPRESSION,
            encoding=self.ENCODING,
            enqueue=True,
            filter=lambda record: record["level"].name == "INFO" or record["level"].name == "DEBUG"
        )

        # 3. 错误日志文件 (Error 及以上)
        error_log_file = self.LOG_PATH / "{time:YYYY-MM-DD}_error.log"
        logger.add(
            str(error_log_file),
            level="ERROR",
            format=self.FORMAT,
            rotation=self.ROTATION, # 按大小轮转，防止错误日志过大
            retention=self.RETENTION,
            compression=self.COMPRESSION,
            encoding=self.ENCODING,
            enqueue=True,
            backtrace=True, # 记录异常堆栈
            diagnose=True   # 记录变量值 (生产环境可视情况关闭)
        )

    @staticmethod
    def get_logger():
        return logger

# 初始化日志配置
# 你可以在 main.py 或 app 启动时调用 LogConfig(level="DEBUG")
# 这里默认初始化，保证导入即用
log_config = LogConfig(level="DEBUG")

# 导出 logger 供其他模块使用
__all__ = ["logger", "LogConfig"]
