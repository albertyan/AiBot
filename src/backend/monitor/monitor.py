import time
import threading
from typing import Dict
from loguru import logger
from auto.pyweixin.utils import scan_for_new_messages
from auto.pyweixin.WeChatTools import Navigator
from .message_manager import message_manager

class WeChatMonitor:
    """
    微信消息监控器
    每隔一定时间检查是否有新消息
    """
    def __init__(self, interval: int = 5):
        self.interval = interval
        self.running = False
        self.thread = None
        self._stop_event = threading.Event()

    def start(self):
        """启动监控"""
        if self.running:
            logger.warning("WeChat monitor is already running.")
            return

        self.running = True
        self._stop_event.clear()
        self.thread = threading.Thread(target=self._run_loop, name="WeChatMonitorThread", daemon=True)
        self.thread.start()
        logger.info(f"WeChat monitor started with interval {self.interval}s.")

    def stop(self):
        """停止监控"""
        if not self.running:
            return
            
        self.running = False
        self._stop_event.set()
        if self.thread:
            self.thread.join(timeout=2)
        logger.info("WeChat monitor stopped.")

    def _run_loop(self):
        """监控循环"""
        logger.info("WeChat monitor loop started.")
        while self.running:
            try:
                if self._stop_event.is_set():
                    break

                # 检查新消息
                # 注意：scan_for_new_messages 可能会打开微信窗口并置顶
                # close_weixin=False 避免每次检查完关闭微信
                logger.debug("Scanning for new WeChat messages...")
                
                # 获取主窗口对象，避免每次重新查找（但这取决于scan_for_new_messages内部是否使用了缓存）
                # scan_for_new_messages 内部如果 main_window 为 None 会自动打开
                new_messages = scan_for_new_messages(close_weixin=False)
                
                if new_messages:
                    logger.info(f"New messages found: {new_messages}")
                    # 处理新消息
                    try:
                        message_manager.handle_messages(new_messages)
                    except Exception as e:
                        logger.error(f"Error handling messages: {e}")
                
            except Exception as e:
                logger.error(f"Error during WeChat scan: {e}")
            
            # 等待间隔
            self._stop_event.wait(self.interval)

# 全局单例
monitor = WeChatMonitor()


