from __future__ import annotations
from pydantic import BaseModel, Field
from .base import JSONConfigStore

class MomentSettings(BaseModel):
    """
    朋友圈交互配置
    为什么集中在模型：便于API层做整体校验与版本演进
    """
    agentId: str = Field(default="")
    commentLimit: int = Field(default=10)
    perFriendLimit: int = Field(default=3)
    autoLike: bool = Field(default=True)
    interactionMode: str = Field(default="like_only")
    blacklist: str = Field(default="")
    prompt: str = Field(default="")

class MomentSettingsWrapper(BaseModel):
    moment_settings: MomentSettings = Field(default_factory=MomentSettings)

class MomentSettingsStore(JSONConfigStore):
    """
    moment_settings.json 存取与操作
    """
    def __init__(self):
        super().__init__("moment_settings.json")

    def load(self) -> MomentSettings:
        wrapped = self.load_model(MomentSettingsWrapper, root_key=None, default={})
        return wrapped.moment_settings

    def view(self) -> MomentSettings:
        return self.load()

    def save(self, settings: MomentSettings) -> None:
        self.save_model(MomentSettingsWrapper(moment_settings=settings))

    def update(self, patch: dict) -> MomentSettings:
        current = self.load()
        base = current.model_dump()
        base.update(patch or {})
        updated = MomentSettings(**base)
        self.save(updated)
        return updated
