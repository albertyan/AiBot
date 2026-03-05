from __future__ import annotations
from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from .base import JSONConfigStore

class GreetingItem(BaseModel):
    """
    话术条目
    为什么允许可选字段：不同类型的条目字段不同，统一模型便于列表管理
    """
    type: Literal["file", "text", "agent"] = Field(default="text")
    content: str = Field(default="")
    filePath: Optional[str] = None
    agentId: Optional[str] = None
    prompt: Optional[str] = None

class GreetingGroup(BaseModel):
    name: str = Field(default="")
    greetings: List[GreetingItem] = Field(default_factory=list)

class GreetingConfig(BaseModel):
    greeting_config: List[GreetingGroup] = Field(default_factory=list)

class GreetingConfigStore(JSONConfigStore):
    """
    greeting_config.json 存取与操作
    """
    def __init__(self):
        super().__init__("greeting_config.json")

    def load(self) -> GreetingConfig:
        return self.load_model(GreetingConfig, root_key=None, default={"greeting_config": []})

    def view(self) -> GreetingConfig:
        return self.load()

    def save(self, cfg: GreetingConfig) -> None:
        self.save_model(cfg)

    def add_group(self, group: GreetingGroup) -> GreetingConfig:
        cfg = self.load()
        cfg.greeting_config.append(group)
        self.save(cfg)
        return cfg

    def remove_group(self, group_name: str) -> GreetingConfig:
        cfg = self.load()
        cfg.greeting_config = [g for g in cfg.greeting_config if g.name != group_name]
        self.save(cfg)
        return cfg

    def add_item(self, group_name: str, item: GreetingItem) -> GreetingConfig:
        cfg = self.load()
        for g in cfg.greeting_config:
            if g.name == group_name:
                g.greetings.append(item)
                break
        self.save(cfg)
        return cfg

    def remove_item(self, group_name: str, index: int) -> GreetingConfig:
        cfg = self.load()
        for g in cfg.greeting_config:
            if g.name == group_name and 0 <= index < len(g.greetings):
                g.greetings.pop(index)
                break
        self.save(cfg)
        return cfg
