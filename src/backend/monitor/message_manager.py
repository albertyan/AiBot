import json
import os
import re
import time
from typing import Dict, List, Tuple
from abc import ABC, abstractmethod
from loguru import logger
from .message_adapter import message_adapter
from websocket.ws_manager import ws_manager


class MessageFilter(ABC):
    """
    消息过滤策略
    为什么使用策略：将不同维度的过滤条件解耦，便于增删与组合，避免在一个方法里堆叠条件。
    """
    @abstractmethod
    def allow(self, sender: str, content: str, common_config: dict) -> bool:
        pass

class ColleagueIgnoreFilter(MessageFilter):
    """忽略同事名单"""
    def allow(self, sender: str, content: str, common_config: dict) -> bool:
        raw = common_config.get("colleagueNamesToIgnore", "")
        ignores = [name.strip() for name in raw.split("//") if name.strip()]
        return sender not in ignores

class WhitelistFilter(MessageFilter):
    """白名单控制"""
    def allow(self, sender: str, content: str, common_config: dict) -> bool:
        wl = common_config.get("whitelist", {}) or {}
        enabled = bool(wl.get("enabled", False))
        if not enabled:
            return True
        whitelist = wl.get("list", []) or []
        return sender in whitelist

class KeywordFilter(MessageFilter):
    """敏感词过滤"""
    def allow(self, sender: str, content: str, common_config: dict) -> bool:
        words = common_config.get("filterWords", []) or []
        for w in words:
            if w and w in str(content):
                return False
        return True

class BaseMessageParser(ABC):
    """
    消息解析模板
    为什么使用模板方法：固定解析流程的骨架（预处理→识别类型→构造结构），具体细节由子类覆写，便于扩展。
    """
    time_patterns = [
        re.compile(r"^\s*\d{1,2}:\d{2}\s*$"),
        re.compile(r"^\s*昨天\s+\d{1,2}:\d{2}\s*$"),
        re.compile(r"^\s*星期[一二三四五六日]\s+\d{1,2}:\d{2}\s*$"),
        re.compile(r"^\s*(\d{4}年)?\d{1,2}月\d{1,2}日(\s+\d{1,2}:\d{2})?\s*$")
    ]

    def parse(self, sender: str, content: str) -> dict:
        sender, content = self.preprocess(sender, content)
        msg_type = "time" if self.is_time(content) else "text"
        return self.build_record(sender, content, msg_type)

    def preprocess(self, sender: str, content: str) -> tuple[str, str]:
        # 为什么做预处理：统一空白与类型，避免后续判断产生偶发错误
        return str(sender or "").strip(), str(content or "").strip()

    def is_time(self, content: str) -> bool:
        for p in self.time_patterns:
            if p.match(content):
                return True
        return False

    @abstractmethod
    def build_record(self, sender: str, content: str, msg_type: str) -> dict:
        pass

class SimpleWeChatParser(BaseMessageParser):
    """针对当前 WeChat 新消息格式的最小实现"""
    def build_record(self, sender: str, content: str, msg_type: str) -> dict:
        # 为什么结构这样定义：贴合前端最小展示需要，后续可按需扩展字段
        return {
            "sender": sender,
            "content": content,
            "type": msg_type
        }

class MessageManager:
    """
    消息管理器
    负责加载配置并过滤/分发消息
    """
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), "reply_strategy_v2.json")
        self.config = {}
        self.load_config()
        # 为什么在构造函数初始化：避免每次处理都创建对象，降低开销且便于统一配置注入
        self.filters: List[MessageFilter] = [
            ColleagueIgnoreFilter(),
            WhitelistFilter(),
            KeywordFilter(),
        ]
        self.parser: BaseMessageParser = SimpleWeChatParser()
        # 增量去重状态：记录每个 sender 最近一次扫描的“未读条数”或内容指纹
        # 为什么使用去重：微信侧每轮扫描返回的是快照，若不做比对会重复处理相同消息；通过“未读条数/指纹”只处理增量，避免重复回复/广播
        self._last_state: Dict[str, Dict[str, int | str]] = {}
        self._count_re = re.compile(r"\[(\d+)条\]")

    def load_config(self):
        """加载配置文件"""
        if not os.path.exists(self.config_path):
            logger.warning(f"Config file not found: {self.config_path}")
            return

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            logger.info(f"Loaded config from {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to load config: {e}")

    def handle_messages(self, sender, new_messages):
        """
        处理新消息
        为什么在此处编排：集中调用过滤策略与解析模板，便于统一维护与调试
        每次只处理一个对话的消息
        1. 过滤：根据配置的策略（如白名单、敏感词）判断是否允许处理
        2. 发送给websocket，前端展示
        3. 调用智能体：根据配置的智能体类型（如本地/远程）调用智能体处理消息
        4. 智能体回复：根据智能体返回结果，格式化回复内容
        Args:
            sender: 消息发送者  京兆瓦肆
            new_messages: 消息列表  例 [('京兆瓦肆', '好的'), ('albertyanm', '你好')]
        """
        # 每次处理前重新加载配置，以便实时生效（或者可以通过监听文件变化来优化）
        self.load_config()
        common_config = self.config.get("commonConfig", {}) or {}

        if not sender:
            return

        if not isinstance(new_messages, list) or len(new_messages) < 1:
            return

        sender = str(sender or "").strip()

        normalized: List[tuple[str, str]] = []
        for item in new_messages:
            if not isinstance(item, tuple) or len(item) < 2:
                continue
            msg_sender, content = item[0], item[1]
            msg_sender = str(msg_sender or "").strip()
            content = str(content or "").strip()
            if content:
                normalized.append((msg_sender, content))

        if not normalized:
            return

        newest_sender, newest_content = normalized[0]
        newest_fp = f"{newest_sender}|{newest_content}|{len(normalized)}"

        # 为什么做去重：监控线程是周期性扫描，若同一轮快照被重复读取，会导致重复推送/重复触发智能体。
        last_fp = str(self._last_state.get(sender, {}).get("fp", ""))
        if last_fp and last_fp == newest_fp:
            return
        self._last_state[sender] = {"fp": newest_fp}

        inbound_content = None
        for msg_sender, content in normalized:
            if msg_sender == sender:
                inbound_content = content
                break

        if inbound_content is not None:
            for f in self.filters:
                if not f.allow(sender, inbound_content, common_config):
                    logger.debug(f"Filtered by {f.__class__.__name__}: sender={sender}")
                    return

        # 2. 发送给 websocket：前端只识别 refresh_weixin_messages，因此这里构造最小会话结构
        # 为什么构造最小字段：pull_messages 返回的是对话内容，不具备完整会话元数据；先保证 UI 能看到“最新一句”，其余字段留空不阻塞流程。
        try:
            ws_manager.broadcast_threadsafe({
                "type": "wechat_chat_messages",
                "data": {
                    "messages": [{
                        "id": sender,
                        "name": sender,
                        "count": 0,
                        "last_message": newest_content,
                        "last_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        "is_top": False,
                        "raw_content": newest_content,
                        "source": "",
                        "is_group": False
                    }]
                }
            }, topic="wechat_messages")
        except Exception as e:
            logger.error(f"WS broadcast failed: {e}")

        try:
            ws_manager.broadcast_threadsafe({
                "type": "wechat_chat_messages",
                "data": {
                    "sender": sender,
                    "messages": [[s, c] for s, c in normalized]
                }
            }, topic="wechat_messages")
        except Exception as e:
            logger.error(f"WS broadcast failed: {e}")

        # 3. 调用智能体：交由适配器异步编排，避免在监控线程里做重任务导致卡顿/误判超时
        if inbound_content is not None:
            try:
                message_adapter.add_job(sender, inbound_content, self.config)
            except Exception as e:
                logger.error(f"Submit message job failed: {e}")

message_manager = MessageManager()
