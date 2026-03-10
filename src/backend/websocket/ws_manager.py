import asyncio
from typing import Any, Set, Dict
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
        self._topics: Dict[WebSocket, Set[str]] = {}
        self.loop: asyncio.AbstractEventLoop | None = None
        self._lock = asyncio.Lock()

    def set_loop(self, loop: asyncio.AbstractEventLoop):
        # 为什么存事件循环：允许在非事件循环线程（如监控线程）安全地调度广播任务
        self.loop = loop

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        async with self._lock:
            self.active.add(websocket)
            self._topics[websocket] = set()
        logger.info(f"WebSocket connected, total={len(self.active)}")

    async def disconnect(self, websocket: WebSocket):
        async with self._lock:
            if websocket in self.active:
                self.active.remove(websocket)
            if websocket in self._topics:
                del self._topics[websocket]
        logger.info(f"WebSocket disconnected, total={len(self.active)}")

    async def subscribe(self, websocket: WebSocket, topics: list[str]):
        """
        订阅指定主题
        为什么需要主题：同一路由可能被多个页面复用，但不同页面只应接收自己关心的推送，避免“全量广播”导致 UI 干扰。
        """
        clean = [str(t or "").strip() for t in (topics or [])]
        clean = [t for t in clean if t]
        if not clean:
            return
        async with self._lock:
            if websocket not in self._topics:
                self._topics[websocket] = set()
            for t in clean:
                self._topics[websocket].add(t)

    async def broadcast(self, data: Any, topic: str | None = None):
        """
        广播 JSON 数据到所有连接
        为什么逐个发送：确保单个连接异常不影响其他连接；失败的连接会被移除
        """
        to_remove = []
        async with self._lock:
            for ws in list(self.active):
                if topic:
                    topics = self._topics.get(ws, set())
                    if topic not in topics:
                        continue
                try:
                    await ws.send_json(data)
                except Exception:
                    to_remove.append(ws)
            for ws in to_remove:
                if ws in self.active:
                    self.active.remove(ws)
                if ws in self._topics:
                    del self._topics[ws]
        if to_remove:
            logger.warning(f"Removed {len(to_remove)} broken WebSocket(s)")

    def broadcast_threadsafe(self, data: Any, topic: str | None = None):
        """
        在线程安全的上下文中广播
        为什么使用 run_coroutine_threadsafe：允许在后台线程（如监控）触发广播
        """
        if self.loop is None:
            logger.debug("WSManager loop not set; drop message")
            return
        try:
            asyncio.run_coroutine_threadsafe(self.broadcast(data, topic=topic), self.loop)
        except Exception as e:
            logger.error(f"Failed to submit WS broadcast: {e}")

# 单例实例，供全局引用
ws_manager = WSManager()
