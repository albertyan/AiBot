from __future__ import annotations
from pydantic import BaseModel, Field
from .base import JSONConfigStore

class CozeSettings(BaseModel):
    """
    Coze 平台配置
    为什么最小化：仅保留需要用到的关键字段
    """
    token: str = Field(default="")
    last_update_time: str = Field(default="")

class CozeSettingsStore(JSONConfigStore):
    """
    coze_settings.json 存取与操作
    """
    def __init__(self):
        super().__init__("coze_settings.json")

    def load(self) -> CozeSettings:
        return self.load_model(CozeSettings, root_key=None, default={})

    def view(self) -> CozeSettings:
        return self.load()

    def save(self, settings: CozeSettings) -> None:
        self.save_model(settings)

    def update(self, patch: dict) -> CozeSettings:
        current = self.load()
        base = current.model_dump() if hasattr(current, "model_dump") else current.dict()
        base.update(patch or {})
        updated = CozeSettings(**base)
        self.save(updated)
        return updated
