import json
import os
import time
from fastapi import APIRouter, Depends

from environment import CurrentUserDep
from utils.response_util import ResponseUtil
from utils.config_file import get_personal_dir
from .schemas import CommonConfig, StaffAgent, AgentId, UpdateEnableStatus, MonitorControl
from monitor.monitor import monitor


aisale_router = APIRouter()


# AI 助理配置（每个用户独立）
@aisale_router.get("/get_ai_config")
async def get_ai_config(current_user: CurrentUserDep):
    '''
    获取AI配置
    配置文件示例 reply_stategy.json
    '''
    # 判断 reply_stategy.json 是否存在
    if not os.path.exists(os.path.join(get_personal_dir(current_user.wxNumber), "reply_stategy.json")):
        return ResponseUtil.success(data={"config": {}})
    
    try:
        with open(os.path.join(get_personal_dir(current_user.wxNumber), "reply_stategy.json"), "r", encoding='utf-8') as f:
            data = json.load(f)
    except:
        return ResponseUtil.error(msg="reply_stategy.json 格式错误")
    
    return ResponseUtil.success(data={"config": data})

@aisale_router.post("/save_agent")
async def save_agent(current_user: CurrentUserDep, agent: StaffAgent):
    '''
    添加智能体
    '''
    personal_dir = get_personal_dir(current_user.wxNumber)
    file_path = os.path.join(personal_dir, "reply_stategy.json")

    data = {"staffList": [], "commonConfig": {}}
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                data["staffList"] = loaded.get("staffList", []) if isinstance(loaded.get("staffList"), list) else []
                data["commonConfig"] = loaded.get("commonConfig", {}) if isinstance(loaded.get("commonConfig"), dict) else {}
        except Exception:
            return ResponseUtil.error(msg="reply_stategy.json 格式错误")
    
    # Process the new/updated agent
    agent_dict = agent.model_dump()
    
    # Generate ID if missing
    if not agent_dict.get("id"):
        agent_dict["id"] = str(int(time.time() * 1000))
    else:
        agent_dict["id"] = str(agent_dict["id"])

    # Ensure other fields are strings where necessary
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
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return ResponseUtil.error(msg=f"保存失败: {e}")

    return ResponseUtil.success(data={"staffList": staff_list})


@aisale_router.post("/delete_agent")
async def delete_agent(current_user: CurrentUserDep, data_in: AgentId):
    '''
    删除智能体
    '''
    agent_id = data_in.agent_id
    if not agent_id:
        return ResponseUtil.error(msg="智能体ID不能为空")

    personal_dir = get_personal_dir(current_user.wxNumber)
    file_path = os.path.join(personal_dir, "reply_stategy.json")

    data = {"staffList": [], "commonConfig": {}}
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                data["staffList"] = loaded.get("staffList", []) if isinstance(loaded.get("staffList"), list) else []
                data["commonConfig"] = loaded.get("commonConfig", {}) if isinstance(loaded.get("commonConfig"), dict) else {}
        except Exception:
            return ResponseUtil.error(msg="reply_stategy.json 格式错误")
            
    staff_list = data.get("staffList", [])
    # Filter out the agent to delete
    new_staff_list = [item for item in staff_list if str(item.get("id")) != str(agent_id)]
    
    data["staffList"] = new_staff_list
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return ResponseUtil.error(msg=f"删除失败: {e}")

    return ResponseUtil.success(data={"staffList": new_staff_list})

@aisale_router.post("/save_common_config")
async def save_common_config(current_user: CurrentUserDep, config: CommonConfig):
    '''
    保存通用配置
    '''
    personal_dir = get_personal_dir(current_user.wxNumber)
    file_path = os.path.join(personal_dir, "reply_stategy.json")

    data = {"staffList": [], "commonConfig": {}}
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                data["staffList"] = loaded.get("staffList", []) if isinstance(loaded.get("staffList"), list) else []
                data["commonConfig"] = loaded.get("commonConfig", {}) if isinstance(loaded.get("commonConfig"), dict) else {}
        except Exception:
            return ResponseUtil.error(msg="reply_stategy.json 格式错误")
    
    data["commonConfig"] = config.model_dump()
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return ResponseUtil.error(msg=f"保存失败: {e}")

    return ResponseUtil.success(data={"commonConfig": data["commonConfig"]})

@aisale_router.post("/update_enable_status")
async def update_enable_status(current_user: CurrentUserDep, status: UpdateEnableStatus):
    '''
    更新启用状态
    '''
    personal_dir = get_personal_dir(current_user.wxNumber)
    file_path = os.path.join(personal_dir, "reply_stategy.json")

    data = {"staffList": [], "commonConfig": {}}
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                data["staffList"] = loaded.get("staffList", []) if isinstance(loaded.get("staffList"), list) else []
                data["commonConfig"] = loaded.get("commonConfig", {}) if isinstance(loaded.get("commonConfig"), dict) else {}
        except Exception:
            return ResponseUtil.error(msg="reply_stategy.json 格式错误")
    
    staff_list = data.get("staffList", [])
    found = False
    for agent in staff_list:
        if str(agent.get("id")) == str(status.agent_id):
            agent["enabled"] = status.enabled
            found = True
            break
            
    if not found:
        return ResponseUtil.error(msg="未找到指定智能体")
        
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return ResponseUtil.error(msg=f"保存失败: {e}")

    return ResponseUtil.success()

@aisale_router.post("/refresh_weixin_messages")
async def refresh_weixin_messages(current_user: CurrentUserDep):
    '''
    刷新微信消息
    '''
    from auto.pyweixin.utils import scan_for_new_messages
    newMessages_dict=scan_for_new_messages()
    return ResponseUtil.success(data={"newMessages_dict": newMessages_dict})

@aisale_router.post("/toggle_monitor")
async def toggle_monitor(current_user: CurrentUserDep, data: MonitorControl):
    """
    开启或关闭微信消息监控
    """
    if data.enabled:
        monitor.start()
        msg = "监控已启动"
    else:
        monitor.stop()
        msg = "监控已停止"
    
    return ResponseUtil.success(msg=msg)

@aisale_router.get("/get_monitor_status")
async def get_monitor_status(current_user: CurrentUserDep):
    """
    获取微信消息监控状态
    """
    return ResponseUtil.success(data={"enabled": monitor.running})
