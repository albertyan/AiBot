from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field, EmailStr
from .base import JSONConfigStore

class AlertSettings(BaseModel):
    """
    预警配置
    为什么用Pydantic：在修改配置时即可校验合法性，防止脏数据落盘
    """
    email: EmailStr = Field(default="example@example.com")
    frequency: Literal["immediate", "daily", "weekly"] = Field(default="immediate")
    enabled: bool = Field(default=True)

class AlertSettingsWrapper(BaseModel):
    alert_settings: AlertSettings = Field(default_factory=AlertSettings)

class AlertSettingsStore(JSONConfigStore):
    """
    alert_settings.json 存取与操作
    为什么单一类：聚焦一个配置文件的增删改查
    """
    def __init__(self):
        super().__init__("alert_settings.json")

    def load(self) -> AlertSettings:
        wrapped = self.load_model(AlertSettingsWrapper, root_key=None, default={})
        return wrapped.alert_settings

    def view(self) -> AlertSettings:
        return self.load()

    def save(self, settings: AlertSettings) -> None:
        self.save_model(AlertSettingsWrapper(alert_settings=settings))

    def update(self, patch: dict) -> AlertSettings:
        data = self.load()
        # 合并更新，保证未提供的字段沿用旧值
        base = data.model_dump()
        base.update(patch or {})
        updated = AlertSettings(**base)
        self.save(updated)
        return updated
