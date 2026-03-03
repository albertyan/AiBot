import os
import json
import time
from typing import Dict, List, Any
from utils.config_file import get_personal_dir
from api.schemas import StaffAgent, CommonConfig
from utils.perf_util import instrument_class

class AiConfigService:
    def __init__(self):
        pass

    def _get_config_path(self, wx_number: str) -> str:
        personal_dir = get_personal_dir(wx_number)
        return os.path.join(personal_dir, "reply_stategy.json")

    def _load_config(self, wx_number: str) -> Dict[str, Any]:
        file_path = self._get_config_path(wx_number)
        if not os.path.exists(file_path):
            return {"staffList": [], "commonConfig": {}}
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                return {
                    "staffList": loaded.get("staffList", []) if isinstance(loaded.get("staffList"), list) else [],
                    "commonConfig": loaded.get("commonConfig", {}) if isinstance(loaded.get("commonConfig"), dict) else {}
                }
            return {"staffList": [], "commonConfig": {}}
        except Exception:
            raise ValueError("reply_stategy.json 格式错误")

    def _save_config(self, wx_number: str, data: Dict[str, Any]):
        file_path = self._get_config_path(wx_number)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise Exception(f"保存失败: {e}")

    def get_ai_config(self, wx_number: str) -> Dict[str, Any]:
        """
        获取AI配置
        """
        try:
            data = self._load_config(wx_number)
            # The original API returns {"config": data}
            # Here we return the data directly, and let the API wrap it
            return data
        except ValueError as e:
            raise e

    def save_agent(self, wx_number: str, agent: StaffAgent) -> List[Dict[str, Any]]:
        """
        保存智能体配置
        """
        data = self._load_config(wx_number)
        
        agent_dict = agent.model_dump()
        if not agent_dict.get("id"):
            agent_dict["id"] = str(int(time.time() * 1000))
        else:
            agent_dict["id"] = str(agent_dict["id"])
        
        agent_dict["agentId"] = str(agent_dict["agentId"])
        
        staff_list = data.get("staffList", [])
        replaced = False
        for idx, item in enumerate(staff_list):
            if str(item.get("id")) == agent_dict["id"]:
                staff_list[idx] = agent_dict
                replaced = True
                break
        
        if not replaced:
            staff_list.append(agent_dict)
            
        data["staffList"] = staff_list
        self._save_config(wx_number, data)
        return staff_list

    def delete_agent(self, wx_number: str, agent_id: str) -> List[Dict[str, Any]]:
        """
        删除智能体
        """
        data = self._load_config(wx_number)
        staff_list = data.get("staffList", [])
        new_staff_list = [item for item in staff_list if str(item.get("id")) != str(agent_id)]
        
        data["staffList"] = new_staff_list
        self._save_config(wx_number, data)
        return new_staff_list

    def save_common_config(self, wx_number: str, config: CommonConfig) -> Dict[str, Any]:
        """
        保存通用配置
        """
        data = self._load_config(wx_number)
        data["commonConfig"] = config.model_dump()
        self._save_config(wx_number, data)
        return data["commonConfig"]

    def update_enable_status(self, wx_number: str, agent_id: str, enabled: bool):
        """
        更新智能体启用状态
        """
        data = self._load_config(wx_number)
        staff_list = data.get("staffList", [])
        found = False
        for agent in staff_list:
            if str(agent.get("id")) == str(agent_id):
                agent["enabled"] = enabled
                found = True
                break
        
        if not found:
            raise ValueError("未找到指定智能体")
            
        self._save_config(wx_number, data)

AiConfigService = instrument_class(AiConfigService, prefix="service.AiConfigService")
ai_config_service = AiConfigService()
