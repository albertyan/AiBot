import time
import threading
from typing import Dict, Any, List
from loguru import logger
import asyncio
import sys
import os

from auto.pyweixin.WeChatTools import Navigator
from service.wechat_service import wechat_service
from service.groups_service import groups_service
from environment import state
from auto.WeChatBot import WeChatBot
from .message_manager import message_manager
import time as _time
from db.database import AsyncSessionLocal


async def _fetch_group_names(wx_number: str) -> set[str]:
    """
    查询该账号的群聊名称集合
    为什么在监控线程侧查询：WebSocket 推送需要与 refresh_weixin_messages 接口输出一致（is_group 标识），
    而 service.get_new_messages 本身只负责解析微信 UI 快照，不包含业务侧的“群聊名单”信息。
    """
    async with AsyncSessionLocal() as db:
        groups = await groups_service.get_all_groups(wx_number, db)
    return {str(g.get("name")) for g in (groups or []) if g and g.get("name")}


def _get_group_names_sync(wx_number: str) -> set[str]:
    """
    在同步线程中执行异步 DB 查询
    为什么不复用 FastAPI 事件循环：监控运行在独立线程，为了避免跨线程调度复杂度，用独立事件循环执行一次性查询更稳妥。
    """
    try:
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(_fetch_group_names(wx_number))
    finally:
        try:
            loop.close()
        except Exception:
            pass

class WeChatMonitor:
    """
    微信消息监控器
    每隔一定时间检查是否有新消息
    """
    def __init__(self, interval: int = 5, scan_timeout: float = 3.0, fail_threshold: int = 3, open_seconds: float = 30.0):
        """
        初始化监控器
        为什么引入超时与熔断参数：
        - scan_timeout：UI 自动化调用可能卡死，限制单次扫描最长耗时，避免阻塞周期
        - fail_threshold：连续异常阈值，超过即熔断，避免频繁无效调用
        - open_seconds：熔断打开时间，给外部环境（微信/UI）恢复的窗口
        """
        self.interval = interval
        self.scan_timeout = scan_timeout
        self.fail_threshold = fail_threshold
        self.open_seconds = open_seconds
        self.running = False
        self.thread = None
        self._stop_event = threading.Event()
        self._fail_count = 0
        self._circuit_until = 0.0
        self.main_window = None  # 复用主窗口句柄，参照示例先在非工作线程打开，降低线程内UI初始化风险

    def start(self):
        """启动监控"""
        if self.running:
            logger.warning("WeChat monitor is already running.")
            return

        # # 参照示例：先在当前线程打开主窗口，再交由后台循环复用
        try:
            # 只唤醒微信，不保存对象供线程使用，避免跨线程问题
            # self.main_window = Navigator.open_weixin(is_maximize=None)
            self.main_window=WeChatBot.find_window()
            logger.debug("Navigator.open_weixin succeeded before starting monitor thread")
        except Exception as e:
            logger.warning(f"open_weixin before monitor thread failed: {e}")
            self.main_window = None

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
        try:
            loop_count = 0
            while not self._stop_event.is_set():
                loop_count += 1
                try:
                    cycle_start = _time.monotonic()
                    if self._stop_event.is_set():
                        logger.info("Stop event set, breaking loop")
                        break

                    # 熔断检查：在打开窗口内跳过扫描，直接进入等待
                    now = _time.monotonic()
                    if now < self._circuit_until:
                        remaining_cooldown = self._circuit_until - now
                        logger.warning(f"Circuit open, skip scan for {remaining_cooldown:.1f}s")
                        self._stop_event.wait(min(remaining_cooldown, self.interval))
                        continue

                    # 检查新消息
                    logger.debug(f"Loop #{loop_count}: Scanning for new WeChat messages...")
                    
                    scan_start = _time.monotonic()
                    try:
                        # 复用 service 层方法：统一解析会话快照
                        user = state.get_current_user()
                        if not user or not user.wxNumber:
                            logger.warning("No current user bound; skip scan")
                            self._stop_event.wait(self.interval)
                            continue
                        
                        logger.debug(f"Loop #{loop_count}: Calling get_new_messages...")
                        # 避免跨线程传递窗口对象：在当前线程内创建/查找
                        sessions = wechat_service.get_new_messages(user.wxNumber, self.main_window)
                        logger.debug(f"Loop #{loop_count}: get_new_messages returned {len(sessions) if sessions else 0} sessions")

                        for s in sessions or []:
                            if s.name:
                                logger.debug(f"Session sender: {s.model_dump_json()}")
                                logger.debug(f"Session name: {s.name}")
                                _time.sleep(0.5)
                                msgs = WeChatBot.pull_messages(
                                    s.name,
                                    user.wxNickname,
                                    number=8,
                                    search_pages=0,
                                    is_maximize=False,
                                    close_weixin=False,
                                    main_window=self.main_window  # 复用主窗口句柄
                                )
                                logger.debug(f"Session new_messages: {msgs}")

                    except Exception as e:
                        logger.exception(f"get_new_messages failed: {e}")
                        self._stop_event.wait(self.interval)
                        continue
                    
                    new_messages = sessions
                    if sessions:
                        try:
                            logger.debug(f"Loop #{loop_count}: Fetching group names...")
                            group_names = _get_group_names_sync(user.wxNumber)
                            for s in sessions:
                                if s.name in group_names:
                                    s.is_group = True
                            logger.debug(f"Loop #{loop_count}: Group names fetched")
                        except Exception as e:
                            logger.warning(f"Load group names failed, fallback is_group=False: {e}")
                    scan_cost = _time.monotonic() - scan_start
                    if scan_cost > self.scan_timeout:
                        self._fail_count += 1
                        logger.error(f"WeChat scan slow {scan_cost:.2f}s > {self.scan_timeout}s (fail_count={self._fail_count})")
                        if self._fail_count >= self.fail_threshold:
                            self._circuit_until = _time.monotonic() + self.open_seconds
                            logger.error(f"Circuit opened for {self.open_seconds}s due to consecutive slow scans")
                        continue
                    else:
                        self._fail_count = 0
                except Exception as e:
                    self._fail_count += 1
                    logger.exception(f"WeChat scan failed: {e} (fail_count={self._fail_count})")
                    if self._fail_count >= self.fail_threshold:
                        self._circuit_until = _time.monotonic() + self.open_seconds
                        logger.error(f"Circuit opened for {self.open_seconds}s due to consecutive failures")
                    continue
                logger.debug(f"Loop #{loop_count}: Scan finished")
                
                if new_messages:
                    logger.info(f"New messages found: {new_messages}")
                    try:
                        message_manager.handle_messages(new_messages)
                    except Exception as e:
                        logger.error(f"Error handling messages: {e}")
                # 等待间隔
                elapsed = _time.monotonic() - cycle_start
                remaining = max(0.0, self.interval - elapsed)
                logger.debug(f"Loop #{loop_count}: Sleeping for {remaining:.2f}s")
                self._stop_event.wait(remaining)
        finally:
            try:
                import comtypes
                comtypes.CoUninitialize()
                logger.debug("COM uninitialized in monitor thread")
            except Exception:
                pass

# 全局单例
monitor = WeChatMonitor(
    interval=5,
    scan_timeout=6.0,   # 为什么设为6秒：适配实际UI耗时，避免正常情况下误触超时
    fail_threshold=5,   # 为什么调高至5：减少短暂波动导致的频繁熔断
    open_seconds=15.0   # 为什么缩短至15秒：更快恢复尝试，兼顾保护与可用性
)
