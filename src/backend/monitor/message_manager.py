import json
import os
import re
from typing import Dict, List
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

    def handle_messages(self, new_messages: Dict[str, str]):
        """
        处理新消息
        为什么在此处编排：集中调用过滤策略与解析模板，便于统一维护与调试
        Args:
            new_messages: {sender_name: message_text_or_count}
        """
        # 每次处理前重新加载配置，以便实时生效（或者可以通过监听文件变化来优化）
        self.load_config()
        common_config = self.config.get("commonConfig", {}) or {}

        parsed_items = []
        for sender, content in new_messages.items():
            # 1. 按策略链过滤
            allowed = True
            for f in self.filters:
                if not f.allow(sender, content, common_config):
                    allowed = False
                    logger.debug(f"Filtered by {f.__class__.__name__}: sender={sender}")
                    break
            if not allowed:
                continue

            # 2. 解析为统一结构（模板方法）
            parsed = self.parser.parse(sender, content)
            parsed_items.append(parsed)

            # 3. 提交给业务适配器处理（如自动回复、记录等）
            logger.info(f"Processing message from {sender}")
            message_adapter.add_job(sender, content, self.config)

        # 4. 通过 WebSocket 广播给前端（只广播通过过滤并解析完成的消息）
        if parsed_items:
            try:
                ws_manager.broadcast_threadsafe({
                    "type": "new_messages",
                    "items": parsed_items
                })
            except Exception as e:
                logger.error(f"WS broadcast failed: {e}")

message_manager = MessageManager()
