import asyncio
from typing import Any, Set
from fastapi import WebSocket
from loguru import logger

class WSManager:
    """
    WebSocket 连接管理器
    为什么单独抽离：遵循“每文件一个对象”的单一职责原则，便于在路由、服务层复用；
    并统一管理事件循环与线程安全广播，避免分散实现导致行为不一致。
    """
    def __init__(self):
        self.active: Set[WebSocket] = set()
        self.loop: asyncio.AbstractEventLoop | None = None
        self._lock = asyncio.Lock()

    def set_loop(self, loop: asyncio.AbstractEventLoop):
        # 为什么存事件循环：允许在非事件循环线程（如监控线程）安全地调度广播任务
        self.loop = loop

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        async with self._lock:
            self.active.add(websocket)
        logger.info(f"WebSocket connected, total={len(self.active)}")

    async def disconnect(self, websocket: WebSocket):
        async with self._lock:
            if websocket in self.active:
                self.active.remove(websocket)
        logger.info(f"WebSocket disconnected, total={len(self.active)}")

    async def broadcast(self, data: Any):
        """
        广播 JSON 数据到所有连接
        为什么逐个发送：确保单个连接异常不影响其他连接；失败的连接会被移除
        """
        to_remove = []
        async with self._lock:
            for ws in list(self.active):
                try:
                    await ws.send_json(data)
                except Exception:
                    to_remove.append(ws)
            for ws in to_remove:
                if ws in self.active:
                    self.active.remove(ws)
        if to_remove:
            logger.warning(f"Removed {len(to_remove)} broken WebSocket(s)")

    def broadcast_threadsafe(self, data: Any):
        """
        在线程安全的上下文中广播
        为什么使用 run_coroutine_threadsafe：允许在后台线程（如监控）触发广播
        """
        if self.loop is None:
            logger.debug("WSManager loop not set; drop message")
            return
        try:
            asyncio.run_coroutine_threadsafe(self.broadcast(data), self.loop)
        except Exception as e:
            logger.error(f"Failed to submit WS broadcast: {e}")

# 单例实例，供全局引用
ws_manager = WSManager()
