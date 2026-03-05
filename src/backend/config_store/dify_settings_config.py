from __future__ import annotations
from pydantic import BaseModel, Field, AnyUrl
from .base import JSONConfigStore

class DifySettings(BaseModel):
    """
    Dify 平台配置
    为什么单独配置：不同平台字段不同，保持独立模型更清晰
    """
    baseUrl: str = Field(default="")

class DifySettingsStore(JSONConfigStore):
    """
    dify_settings.json 存取与操作
    """
    def __init__(self):
        super().__init__("dify_settings.json")

    def load(self) -> DifySettings:
        return self.load_model(DifySettings, root_key=None, default={})

    def view(self) -> DifySettings:
        return self.load()

    def save(self, settings: DifySettings) -> None:
        self.save_model(settings)

    def update(self, patch: dict) -> DifySettings:
        current = self.load()
        base = current.model_dump() if hasattr(current, "model_dump") else current.dict()
        base.update(patch or {})
        updated = DifySettings(**base)
        self.save(updated)
        return updated
