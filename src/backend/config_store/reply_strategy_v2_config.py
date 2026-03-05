from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field
from .base import JSONConfigStore

class StaffRule(BaseModel):
    """
    员工规则
    为什么拆分：staffList 结构复杂，独立模型便于维护
    """
    id: str = Field(default="")
    name: str = Field(default="")
    enabled: bool = Field(default=True)
    agentId: str = Field(default="")
    chatType: str = Field(default="single")
    selectedTags: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)

class AutoGreeting(BaseModel):
    enabled: bool = Field(default=False)
    greetingGroupId: str = Field(default="")

class FileRecognition(BaseModel):
    enabled: bool = Field(default=False)
    fileTypes: List[str] = Field(default_factory=list)
    filePath: str = Field(default="")

class WhiteList(BaseModel):
    enabled: bool = Field(default=False)
    names: Optional[str] = None
    list: List[str] = Field(default_factory=list)

class CommonConfig(BaseModel):
    groupAtOnly: bool = Field(default=False)
    colleagueNamesToIgnore: str = Field(default="")
    filterWords: List[str] = Field(default_factory=list)
    autoGreeting: AutoGreeting = Field(default_factory=AutoGreeting)
    fileRecognition: FileRecognition = Field(default_factory=FileRecognition)
    whitelist: WhiteList = Field(default_factory=WhiteList)

class ReplyStrategyV2(BaseModel):
    staffList: List[StaffRule] = Field(default_factory=list)
    commonConfig: CommonConfig = Field(default_factory=CommonConfig)

class ReplyStrategyV2Store(JSONConfigStore):
    """
    reply_strategy_v2.json 存取与操作
    """
    def __init__(self):
        super().__init__("reply_strategy_v2.json")

    def load(self) -> ReplyStrategyV2:
        return self.load_model(ReplyStrategyV2, root_key=None, default={})

    def view(self) -> ReplyStrategyV2:
        return self.load()

    def save(self, cfg: ReplyStrategyV2) -> None:
        self.save_model(cfg)

    def add_staff(self, staff: StaffRule) -> ReplyStrategyV2:
        cfg = self.load()
        cfg.staffList.append(staff)
        self.save(cfg)
        return cfg

    def update_staff(self, staff_id: str, patch: dict) -> ReplyStrategyV2:
        cfg = self.load()
        for i, s in enumerate(cfg.staffList):
            if s.id == staff_id:
                base = s.model_dump()
                base.update(patch or {})
                cfg.staffList[i] = StaffRule(**base)
                break
        self.save(cfg)
        return cfg

    def remove_staff(self, staff_id: str) -> ReplyStrategyV2:
        cfg = self.load()
        cfg.staffList = [s for s in cfg.staffList if s.id != staff_id]
        self.save(cfg)
        return cfg

    def update_common_config(self, patch: dict) -> ReplyStrategyV2:
        cfg = self.load()
        base = cfg.commonConfig.model_dump()
        base.update(patch or {})
        cfg.commonConfig = CommonConfig(**base)
        self.save(cfg)
        return cfg
