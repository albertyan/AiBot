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

class SettingService:
    def __init__(self):
        pass

    def get_coze_settings(self) -> Dict[str, Any]:
        """
        获取 Coze 的 token 以及最后更新时间
        """
        if not os.path.exists(os.path.join(get_base_dir(), "coze_settings.json")):
            return {"token": "", "last_update_time": ""}
        
        try:
            with open(os.path.join(get_base_dir(), "coze_settings.json"), "r", encoding='utf-8') as f:
                data = json.load(f)
            
            last_update_time = data.get("last_update_time")
            # 计算last_update_time 距离当前时间的天数
            last_update_time_seconds = time.mktime(time.strptime(last_update_time, "%Y-%m-%d %H:%M:%S"))
            current_time_seconds = time.time()
            seconds_since_last_update = current_time_seconds - last_update_time_seconds
            # 转换为天数, 向上取整
            days_since_last_update = math.ceil(seconds_since_last_update / (24 * 60 * 60))
            return {"token": data.get("token"), "last_update_time": days_since_last_update}
        except Exception as e:
            logger.error(f"Error loading coze settings: {e}")
            return {"token": "", "last_update_time": ""}

    def save_coze_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        保存 Coze 的 token
        """
        last_update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        result = {"token": settings.get("token"), "last_update_time": last_update_time}
        
        # 写入配置文件  
        with open(os.path.join(get_base_dir(), "coze_settings.json"), "w", encoding='utf-8') as f:
            json.dump(result, f, indent=4)
            
        return result

    def get_dify_settings(self) -> Dict[str, Any]:
        """
        获取 Dify 的地址
        """
        if not os.path.exists(os.path.join(get_base_dir(), "dify_settings.json")):
            return {"baseUrl": ""}
        try:
            with open(os.path.join(get_base_dir(), "dify_settings.json"), "r", encoding='utf-8') as f:
                data = json.load(f)
            return {"baseUrl": data.get("baseUrl")}
        except Exception:
            raise ValueError("dify_settings.json 格式错误")

    def save_dify_settings(self, baseUrl: str) -> Dict[str, Any]:
        """
        设置 Dify 的地址
        """
        result = {"baseUrl": baseUrl}
        # 写入配置文件  
        with open(os.path.join(get_base_dir(), "dify_settings.json"), "w", encoding='utf-8') as f:
            json.dump(result, f, indent=4)
        return result

    def get_all_agents(self) -> List[Dict[str, Any]]:
        """
        获取所有智能体
        """
        if not os.path.exists(os.path.join(get_base_dir(), "agents.json")):
            return []
        
        try:
            with open(os.path.join(get_base_dir(), "agents.json"), "r", encoding='utf-8') as f:
                data = json.load(f)
            return data.get("agents", [])
        except Exception:
            raise ValueError("agents.json 格式错误")

    def add_agent(self, agent: Dict[str, Any]) -> Dict[str, Any]:
        """
        添加智能体
        """
        if not agent.get("name"):
            raise ValueError("智能体名称不能为空")
        if not agent.get("platform"):
            raise ValueError("平台类型不能为空")

        json_path = os.path.join(get_base_dir(), "agents.json")
        data = {"agents": []}
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding='utf-8') as f:
                    data = json.load(f)
            except:
                pass 
        
        agents = data.get("agents", [])
        
        # 生成 ID
        new_id = str(int(time.time() * 1000))
        agent["id"] = new_id
        
        # 处理默认值逻辑
        if agent.get("isDefault"):
            for a in agents:
                a["isDefault"] = False
                
        agents.append(agent)
        
        with open(json_path, "w", encoding='utf-8') as f:
            json.dump({"agents": agents}, f, indent=4, ensure_ascii=False)
            
        return agent

    def save_agent(self, agent: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        保存智能体
        """
        if not os.path.exists(os.path.join(get_base_dir(), "agents.json")):
            return []
        
        try:
            with open(os.path.join(get_base_dir(), "agents.json"), "r", encoding='utf-8') as f:
                data = json.load(f)
        except:
            raise ValueError("agents.json 格式错误")
        
        agents = data.get("agents", [])
        agents.append(agent)
        
        with open(os.path.join(get_base_dir(), "agents.json"), "w", encoding='utf-8') as f:
            json.dump({"agents": agents}, f, indent=4)
        return agents

    def set_default_agent(self, agent_id: str):
        """
        设置默认智能体
        """
        if not agent_id:
            raise ValueError("智能体ID不能为空")
        
        json_path = os.path.join(get_base_dir(), "agents.json")
        if not os.path.exists(json_path):
            raise ValueError("配置文件不存在")
        
        try:
            with open(json_path, "r", encoding='utf-8') as f:
                data = json.load(f)
        except:
            raise ValueError("agents.json 格式错误")
        
        agents = data.get("agents", [])
        found = False
        
        for agent in agents:
            if agent.get("id") == agent_id:
                found = True
                break
                
        if not found:
            raise ValueError("智能体不存在")

        for agent in agents:
            agent["isDefault"] = (agent.get("id") == agent_id)
        
        with open(json_path, "w", encoding='utf-8') as f:
            json.dump({"agents": agents}, f, indent=4, ensure_ascii=False)

    def delete_agent(self, agent_id: str):
        """
        删除智能体
        """
        if not agent_id:
            raise ValueError("智能体ID不能为空")
        
        json_path = os.path.join(get_base_dir(), "agents.json")
        if not os.path.exists(json_path):
            return 
            
        try:
            with open(json_path, "r", encoding='utf-8') as f:
                data = json.load(f)
                
            agents = data.get("agents", [])
            original_count = len(agents)
            new_agents = [agent for agent in agents if agent.get("id") != agent_id]
            
            if len(new_agents) == original_count:
                return # 没有找到并删除
                
            data["agents"] = new_agents
            with open(json_path, "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error deleting agent: {e}")
            raise e

    def get_greeting_config(self) -> List[Dict[str, Any]]:
        """
        获取话术组配置
        """
        file_path = os.path.join(get_base_dir(), "greeting_config.json")
        if not os.path.exists(file_path):
            raise ValueError("greeting_config.json not found")

        try:
            with open(file_path, "r", encoding='utf-8') as f:
                data = json.load(f)
            
            config = data.get("greeting_config")
            
            if isinstance(config, dict) and "greeting_config" in config:
                config = config["greeting_config"]
                
            if not isinstance(config, list):
                config = []
                
            return config
        except Exception as e:
            logger.error(f"Error loading greeting config: {e}")
            raise ValueError("Failed to load greeting config")

    def save_greeting_config(self, config: Dict[str, Any]):
        """
        保存话术组配置
        """
        with open(os.path.join(get_base_dir(), "greeting_config.json"), "w", encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

    def get_moment_settings(self) -> Dict[str, Any]:
        """
        获取朋友圈评论配置
        """
        file_path = os.path.join(get_base_dir(), "moment_settings.json")
        if not os.path.exists(file_path):
            return {
                "moment_settings": {
                    "commentLimit": 10,
                    "perFriendLimit": 2,
                    "autoLike": False,
                    "interactionMode": "like_and_comment",
                    "blacklist": "",
                    "prompt": "请根据朋友圈的内容，生成一条友善、积极的评论。评论要自然、真诚，避免过于敷衍。如果朋友圈内容是图片，要根据图片内容来评论。",
                    "agentId": ""
                }
            }
        
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading moment settings: {e}")
            raise ValueError("配置文件格式错误")

    def save_moment_settings(self, config: Dict[str, Any]):
        """
        保存朋友圈评论配置
        """
        with open(os.path.join(get_base_dir(), "moment_settings.json"), "w", encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

    def get_chat_history_settings(self) -> Dict[str, Any]:
        """
        获取AI回复配置
        """
        file_path = os.path.join(get_base_dir(), "chat_history_settings.json")
        if not os.path.exists(file_path):
            return {
                "chat_history_settings": {
                    "autoSave": False,
                    "includeContext": True,
                    "contextCount": 7,
                    "includeUserInfo": False,
                    "messageMerge": {
                        "mode": "concat",
                        "interval": 5
                    },
                    "transferConfig": {
                        "phrases": [],
                        "notifyWechat": ""
                    }
                }
            }
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading chat history settings: {e}")
            raise ValueError("配置文件格式错误")

    def save_chat_history_settings(self, config: Dict[str, Any]):
        """
        保存AI回复配置
        """
        with open(os.path.join(get_base_dir(), "chat_history_settings.json"), "w", encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

    def get_alert_settings(self) -> Dict[str, Any]:
        """
        获取预警配置
        """
        file_path = os.path.join(get_base_dir(), "alert_settings.json")
        if not os.path.exists(file_path):
            return {
                "alert_settings": {
                    "email": "albertyan@outlook.com",
                    "frequency": "daily"
                }
            }
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading alert settings: {e}")
            raise ValueError("配置文件格式错误")

    def save_alert_settings(self, config: Dict[str, Any]):
        """
        保存预警配置
        """
        with open(os.path.join(get_base_dir(), "alert_settings.json"), "w", encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

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
        file_path = os.path.join(get_base_dir(), "rest_time_settings.json")
        if not os.path.exists(file_path):
            return {
                "rest_time_settings": {
                    "startTime": 20,
                    "endTime": 8,
                    "selectedTasks": [
                    "自动通过好友",
                    "自动加好友"
                    ]
                }
            }
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading rest time settings: {e}")
            raise ValueError("配置文件格式错误")

    def save_rest_time_settings(self, config: Dict[str, Any]):
        """
        保存休息时间配置
        """
        with open(os.path.join(get_base_dir(), "rest_time_settings.json"), "w", encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

SettingService = instrument_class(SettingService, prefix="service.SettingService")
setting_service = SettingService()
