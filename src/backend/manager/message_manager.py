import json
import os
from typing import Dict, List
from loguru import logger
from adapter.message_adapter import message_adapter

CONFIG_PATH = "/Volumes/work/treaWorkspace/AiBot/.config_file/reply_strategy_v2.json"

class MessageManager:
    """
    消息管理器
    负责加载配置并过滤/分发消息
    """
    def __init__(self):
        self.config_path = CONFIG_PATH
        self.config = {}
        self.load_config()

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
        Args:
            new_messages: {sender_name: message_text_or_count}
        """
        # 每次处理前重新加载配置，以便实时生效（或者可以通过监听文件变化来优化）
        self.load_config()
        
        common_config = self.config.get("commonConfig", {})
        
        # 获取配置项
        colleagues_to_ignore = common_config.get("colleagueNamesToIgnore", "").split("//")
        colleagues_to_ignore = [name.strip() for name in colleagues_to_ignore if name.strip()]
        
        filter_words = common_config.get("filterWords", [])
        
        whitelist_config = common_config.get("whitelist", {})
        whitelist_enabled = whitelist_config.get("enabled", False)
        whitelist = whitelist_config.get("list", [])
        
        for sender, content in new_messages.items():
            # 1. 检查是否在忽略名单中
            if sender in colleagues_to_ignore:
                logger.debug(f"Ignored message from colleague: {sender}")
                continue
                
            # 2. 检查白名单
            if whitelist_enabled and sender not in whitelist:
                logger.debug(f"Ignored message from {sender} (not in whitelist)")
                continue
                
            # 3. 检查过滤词 (content 可能是 "5条新消息" 这种格式，包含最后一条消息内容)
            # 注意：content 是 monitor 传过来的，具体格式取决于 scan_for_new_messages
            # 假设 content 包含消息内容
            should_filter = False
            for word in filter_words:
                if word in str(content):
                    should_filter = True
                    break
            
            if should_filter:
                logger.debug(f"Ignored message from {sender} (contains filter word)")
                continue
                
            # 4. 通过检查，交给适配器处理
            logger.info(f"Processing message from {sender}")
            message_adapter.add_job(sender, content, self.config)

message_manager = MessageManager()
