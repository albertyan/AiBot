from __future__ import annotations
from typing import List
from pydantic import BaseModel, Field
from .base import JSONConfigStore

class RestTimeSettings(BaseModel):
    """
    休息时间配置
    为什么使用字符串时间：便于直接与前端表单绑定，减少转换成本
    """
    startTime: str = Field(default="20:00")
    endTime: str = Field(default="08:00")
    selectedTasks: List[str] = Field(default_factory=list)
    enabled: bool = Field(default=True)

class RestTimeSettingsWrapper(BaseModel):
    rest_time_settings: RestTimeSettings = Field(default_factory=RestTimeSettings)

class RestTimeSettingsStore(JSONConfigStore):
    """
    rest_time_settings.json 存取与操作
    """
    def __init__(self):
        super().__init__("rest_time_settings.json")

    def load(self) -> RestTimeSettings:
        wrapped = self.load_model(RestTimeSettingsWrapper, root_key=None, default={})
        return wrapped.rest_time_settings

    def view(self) -> RestTimeSettings:
        return self.load()

    def save(self, settings: RestTimeSettings) -> None:
        self.save_model(RestTimeSettingsWrapper(rest_time_settings=settings))

    def update(self, patch: dict) -> RestTimeSettings:
        current = self.load()
        base = current.model_dump()
        base.update(patch or {})
        updated = RestTimeSettings(**base)
        self.save(updated)
        return updated
