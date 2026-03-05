from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field
from loguru import logger
from .base import JSONConfigStore

class Agent(BaseModel):
    """
    代理配置项
    为什么结构化：提供明确字段含义与类型约束，避免运行期因格式问题出错
    """
    platform: str = Field(default="")
    name: str = Field(default="")
    botId: str = Field(default="")
    token: str = Field(default="")
    apiKey: str = Field(default="")
    isDefault: bool = Field(default=False)
    id: str = Field(default="")

class AgentsConfig(BaseModel):
    """
    代理配置集合
    为什么单独模型：便于与顶层JSON结构对齐并保证扩展性
    """
    agents: List[Agent] = Field(default_factory=list)

class AgentsConfigStore(JSONConfigStore):
    """
    agents.json 存取与基本操作
    为什么单独类：单一职责聚焦一个配置对象，方法只做一件事
    """
    def __init__(self):
        super().__init__("agents.json")

    def load(self) -> AgentsConfig:
        return self.load_model(AgentsConfig, root_key=None, default={"agents": []})

    def save(self, cfg: AgentsConfig) -> None:
        self.save_model(cfg)

    def view(self) -> AgentsConfig:
        # 为什么提供view别名：语义化的只读获取，便于API层区分
        return self.load()

    def add_agent(self, agent: Agent) -> AgentsConfig:
        cfg = self.load()
        cfg.agents.append(agent)
        self.save(cfg)
        return cfg

    def update_agent(self, agent_id: str, patch: dict) -> AgentsConfig:
        """
        为什么使用patch：允许局部更新，避免调用方必须构造完整对象
        """
        cfg = self.load()
        for idx, a in enumerate(cfg.agents):
            if a.id == agent_id:
                data = a.model_dump()
                data.update(patch or {})
                cfg.agents[idx] = Agent(**data)
                self.save(cfg)
                return cfg
        logger.warning(f"agent not found: {agent_id}")
        return cfg

    def remove_agent(self, agent_id: str) -> AgentsConfig:
        cfg = self.load()
        cfg.agents = [a for a in cfg.agents if a.id != agent_id]
        self.save(cfg)
        return cfg

    def set_default(self, agent_id: str) -> AgentsConfig:
        """
        设置默认代理
        为什么集中处理：保证同时只存在一个默认项
        """
        cfg = self.load()
        found = False
        for a in cfg.agents:
            a.isDefault = (a.id == agent_id)
            if a.isDefault:
                found = True
        if not found:
            logger.warning(f"agent not found for default: {agent_id}")
        self.save(cfg)
        return cfg
