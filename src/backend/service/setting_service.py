import os
import json
import time
import math
import smtplib
from email.mime.text import MIMEText
from typing import Dict, Any, List
from loguru import logger
from utils.config_file import get_base_dir
from utils.perf_util import instrument_class
from config_store.coze_settings_config import CozeSettingsStore, CozeSettings
from config_store.dify_settings_config import DifySettingsStore, DifySettings
from config_store.agents_config import AgentsConfigStore, Agent
from config_store.greeting_config_config import GreetingConfigStore, GreetingConfig, GreetingGroup, GreetingItem
from config_store.moment_settings_config import MomentSettingsStore, MomentSettings, MomentSettingsWrapper
from config_store.chat_history_settings_config import ChatHistorySettingsStore, ChatHistorySettings, ChatHistorySettingsWrapper
from config_store.alert_settings_config import AlertSettingsStore, AlertSettings, AlertSettingsWrapper
from config_store.rest_time_settings_config import RestTimeSettingsStore, RestTimeSettings, RestTimeSettingsWrapper

class SettingService:
    def __init__(self):
        # 为什么在服务层聚合Store：统一对外接口，隐藏具体存储实现，便于后续替换（如DB/远程配置）
        self._coze = CozeSettingsStore()
        self._dify = DifySettingsStore()
        self._agents = AgentsConfigStore()
        self._greeting = GreetingConfigStore()
        self._moment = MomentSettingsStore()
        self._chat_history = ChatHistorySettingsStore()
        self._alert = AlertSettingsStore()
        self._rest_time = RestTimeSettingsStore()

    def get_coze_settings(self) -> Dict[str, Any]:
        """
        获取 Coze 的 token 以及最后更新时间
        """
        try:
            data = self._coze.load()
            if not data.last_update_time:
                return {"token": data.token, "last_update_time": ""}
            last_update_time_seconds = time.mktime(time.strptime(data.last_update_time, "%Y-%m-%d %H:%M:%S"))
            current_time_seconds = time.time()
            seconds_since_last_update = current_time_seconds - last_update_time_seconds
            days_since_last_update = math.ceil(seconds_since_last_update / (24 * 60 * 60))
            return {"token": data.token, "last_update_time": days_since_last_update}
        except Exception as e:
            logger.error(f"Error loading coze settings: {e}")
            return {"token": "", "last_update_time": ""}

    def save_coze_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        保存 Coze 的 token
        """
        last_update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        payload = CozeSettings(token=str(settings.get("token", "")), last_update_time=last_update_time)
        self._coze.save(payload)
        return {"token": payload.token, "last_update_time": payload.last_update_time}

    def get_dify_settings(self) -> Dict[str, Any]:
        """
        获取 Dify 的地址
        """
        data = self._dify.load()
        return {"baseUrl": data.baseUrl}

    def save_dify_settings(self, baseUrl: str) -> Dict[str, Any]:
        """
        设置 Dify 的地址
        """
        model = DifySettings(baseUrl=str(baseUrl))
        self._dify.save(model)
        return {"baseUrl": model.baseUrl}

    def get_all_agents(self) -> List[Dict[str, Any]]:
        """
        获取所有智能体
        """
        cfg = self._agents.view()
        # 返回原始字典列表以兼容现有API
        return [a.model_dump() for a in cfg.agents]

    def add_agent(self, agent: Dict[str, Any]) -> Dict[str, Any]:
        """
        添加智能体
        """
        if not agent.get("name"):
            raise ValueError("智能体名称不能为空")
        if not agent.get("platform"):
            raise ValueError("平台类型不能为空")
        new_id = str(int(time.time() * 1000))
        model = Agent(
            platform=str(agent.get("platform", "")),
            name=str(agent.get("name", "")),
            botId=str(agent.get("botId", "")),
            token=str(agent.get("token", "")),
            apiKey=str(agent.get("apiKey", "")),
            isDefault=bool(agent.get("isDefault", False)),
            id=new_id
        )
        cfg = self._agents.add_agent(model)
        # 如果设置为默认，同步重置其他项
        if model.isDefault:
            self._agents.set_default(new_id)
        return model.model_dump()

    def save_agent(self, agent: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        保存智能体
        """
        # 兼容旧接口：视为新增
        created = self.add_agent(agent)
        return self.get_all_agents()

    def set_default_agent(self, agent_id: str):
        """
        设置默认智能体
        """
        if not agent_id:
            raise ValueError("智能体ID不能为空")
        self._agents.set_default(agent_id)

    def delete_agent(self, agent_id: str):
        """
        删除智能体
        """
        if not agent_id:
            raise ValueError("智能体ID不能为空")
        try:
            self._agents.remove_agent(agent_id)
        except Exception as e:
            logger.error(f"Error deleting agent: {e}")
            raise e

    def get_greeting_config(self) -> List[Dict[str, Any]]:
        """
        获取话术组配置
        """
        cfg = self._greeting.view()
        # 与旧接口兼容，返回列表
        groups = cfg.greeting_config
        return [g.model_dump() for g in groups]

    def save_greeting_config(self, config: Dict[str, Any]):
        """
        保存话术组配置
        """
        # 兼容旧接口：直接落盘完整结构
        try:
            model = GreetingConfig(**config)
            self._greeting.save(model)
        except Exception:
            # 如果字段层级是裸列表（历史版本），做一次兼容转换
            self._greeting.save(GreetingConfig(greeting_config=[GreetingGroup(**g) for g in (config or [])]))

    def get_moment_settings(self) -> Dict[str, Any]:
        """
        获取朋友圈评论配置
        """
        settings = self._moment.load()
        # 保持与旧接口一致的包裹结构
        data = settings.model_dump()
        return {"moment_settings": data}

    def save_moment_settings(self, config: Dict[str, Any]):
        """
        保存朋友圈评论配置
        """
        try:
            wrapped = MomentSettingsWrapper(**config)
            self._moment.save(wrapped.moment_settings)
        except Exception:
            # 兼容直接传 MomentSettings 结构
            self._moment.save(MomentSettings(**config))

    def get_chat_history_settings(self) -> Dict[str, Any]:
        """
        获取AI回复配置
        """
        settings = self._chat_history.load()
        data = settings.model_dump()
        return {"chat_history_settings": data}

    def save_chat_history_settings(self, config: Dict[str, Any]):
        """
        保存AI回复配置
        """
        try:
            wrapped = ChatHistorySettingsWrapper(**config)
            self._chat_history.save(wrapped.chat_history_settings)
        except Exception:
            self._chat_history.save(ChatHistorySettings(**config))

    def get_alert_settings(self) -> Dict[str, Any]:
        """
        获取预警配置
        """
        settings = self._alert.load()
        data = settings.model_dump()
        return {"alert_settings": data}

    def save_alert_settings(self, config: Dict[str, Any]):
        """
        保存预警配置
        """
        try:
            wrapped = AlertSettingsWrapper(**config)
            self._alert.save(wrapped.alert_settings)
        except Exception:
            self._alert.save(AlertSettings(**config))

    def send_test_alert_email(self, email: str):
        """
        发送测试预警邮件
        """
        msg = MIMEText('这是一封测试预警邮件', 'plain', 'utf-8')
        msg['Subject'] = '测试预警邮件'
        msg['From'] = '21145940@qq.com'
        msg['To'] = email
        
        try:
            with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
                server.login('21145940@qq.com', 'alwjookafvbrcabh')
                server.sendmail('21145940@qq.com', email, msg.as_string())
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            raise Exception("发送邮件失败")

    def get_rest_time_settings(self) -> Dict[str, Any]:
        """
        获取休息时间配置
        """
        settings = self._rest_time.load()
        data = settings.model_dump()
        return {"rest_time_settings": data}

    def save_rest_time_settings(self, config: Dict[str, Any]):
        """
        保存休息时间配置
        """
        try:
            wrapped = RestTimeSettingsWrapper(**config)
            self._rest_time.save(wrapped.rest_time_settings)
        except Exception:
            self._rest_time.save(RestTimeSettings(**config))

SettingService = instrument_class(SettingService, prefix="service.SettingService")
setting_service = SettingService()
