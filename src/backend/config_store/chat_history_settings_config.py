from __future__ import annotations
from typing import List, Literal
from pydantic import BaseModel, Field
from .base import JSONConfigStore

class MessageMerge(BaseModel):
    """
    消息合并设置
    为什么拆分子模型：提升可读性与复用性，便于进一步扩展
    """
    mode: Literal["none", "time_window"] = Field(default="none")
    interval: int = Field(default=5)

class TransferConfig(BaseModel):
    phrases: List[str] = Field(default_factory=list)
    notifyWechat: str = Field(default="")

class ChatHistorySettings(BaseModel):
    autoSave: bool = Field(default=False)
    includeContext: bool = Field(default=False)
    contextCount: int = Field(default=5)
    includeUserInfo: bool = Field(default=False)
    messageMerge: MessageMerge = Field(default_factory=MessageMerge)
    transferConfig: TransferConfig = Field(default_factory=TransferConfig)

class ChatHistorySettingsWrapper(BaseModel):
    chat_history_settings: ChatHistorySettings = Field(default_factory=ChatHistorySettings)

class ChatHistorySettingsStore(JSONConfigStore):
    """
    chat_history_settings.json 存取与操作
    """
    def __init__(self):
        super().__init__("chat_history_settings.json")

    def load(self) -> ChatHistorySettings:
        wrapped = self.load_model(ChatHistorySettingsWrapper, root_key=None, default={})
        return wrapped.chat_history_settings

    def view(self) -> ChatHistorySettings:
        return self.load()

    def save(self, settings: ChatHistorySettings) -> None:
        self.save_model(ChatHistorySettingsWrapper(chat_history_settings=settings))

    def update(self, patch: dict) -> ChatHistorySettings:
        current = self.load()
        base = current.model_dump()
        base.update(patch or {})
        updated = ChatHistorySettings(**base)
        self.save(updated)
        return updated
