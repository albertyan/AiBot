import json
import math
import os
from typing import Any
from fastapi import APIRouter
import time

from loguru import logger
from environment import CurrentUserDep
from utils.response_util import ResponseUtil

from utils.config_file import get_base_dir

setting_router = APIRouter()

# AI 接入配置#####################################################################################
@setting_router.get("/coze_settings")
def get_coze_settings(current_user: CurrentUserDep) -> Any:
    '''
    获取 Coze 的 token 以及最后更新时间
    tokenLastUpdated: 距离最后更新时间的天数
    文件示例
    {
        "token": "12345",
        "last_update_time": "2026-02-03 18:16:19"
    }
    '''
    if not os.path.exists(os.path.join(get_base_dir(), "coze_settings.json")):
        return ResponseUtil.success(data={"token": "", "last_update_time": ""})
    
    with open(os.path.join(get_base_dir(), "coze_settings.json"), "r", encoding='utf-8') as f:
        data = json.load(f)
    
    last_update_time = data.get("last_update_time")
    # 计算last_update_time 距离当前时间的天数
    last_update_time_seconds = time.mktime(time.strptime(last_update_time, "%Y-%m-%d %H:%M:%S"))
    current_time_seconds = time.time()
    seconds_since_last_update = current_time_seconds - last_update_time_seconds
    # 转换为天数, 向上取整
    days_since_last_update = math.ceil(seconds_since_last_update / (24 * 60 * 60))
    return ResponseUtil.success(
                   data={"token": data.get("token"), 
                         "last_update_time": days_since_last_update})

@setting_router.post("/coze_settings")
def set_coze_settings(current_user: CurrentUserDep, settings: dict) -> Any:
    '''
    设置 Coze 的 token
    coze_settings.json 示例
    {
        "token": "123434353452345",
        "last_update_time": "2026-01-23 17:28:06"
    }
    '''
    # 这里可以添加逻辑来更新Coze的设置
    # 例如，调用Coze的API来更新设置
    last_update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    result = {"token": settings.get("token"), "last_update_time": last_update_time}
    
    # 写入配置文件  
    with open(os.path.join(get_base_dir(), "coze_settings.json"), "w", encoding='utf-8') as f:
        json.dump(result, f, indent=4)
        
    return ResponseUtil.success(data=result)

@setting_router.post("/dify_settings")
def save_dify_settings(current_user: CurrentUserDep, baseUrl: str) -> Any:
    '''
    设置 Dify 的地址
    dify_settings.json 示例
    {
        "baseUrl": "http://127.0.0.1/v2"
    }
    '''
    # 这里可以添加逻辑来更新Dify的设置
    result = {"baseUrl": baseUrl}
    # 写入配置文件  
    with open(os.path.join(get_base_dir(), "dify_settings.json"), "w", encoding='utf-8') as f:
        json.dump(result, f, indent=4)
    return ResponseUtil.success(data=result)

@setting_router.get("/dify_settings")
def get_dify_settings(current_user: CurrentUserDep) -> Any:
    '''
    获取 Dify 的地址
    '''
    if not os.path.exists(os.path.join(get_base_dir(), "dify_settings.json")):
        return ResponseUtil.success(data={"baseUrl": ""})
    try:
        with open(os.path.join(get_base_dir(), "dify_settings.json"), "r", encoding='utf-8') as f:
            data = json.load(f)
    except:
        return ResponseUtil.error(msg="dify_settings.json 格式错误")
    return ResponseUtil.success(data={"baseUrl": data.get("baseUrl")})

# 智能体管理#####################################################################################
@setting_router.post("/agents")
def add_agent(current_user: CurrentUserDep, agent: dict) -> Any:
    '''
    添加智能体
    '''
    # 验证必要字段
    if not agent.get("name"):
        return ResponseUtil.error(msg="智能体名称不能为空")
    if not agent.get("platform"):
        return ResponseUtil.error(msg="平台类型不能为空")

    # 读取现有数据
    json_path = os.path.join(get_base_dir(), "agents.json")
    data = {"agents": []}
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding='utf-8') as f:
                data = json.load(f)
        except:
            pass # 格式错误则作为空处理
    
    agents = data.get("agents", [])
    
    # 生成 ID
    new_id = str(int(time.time() * 1000))
    agent["id"] = new_id
    
    # 处理默认值逻辑 (如果新添加的是默认，取消其他的默认)
    if agent.get("isDefault"):
        for a in agents:
            a["isDefault"] = False
            
    agents.append(agent)
    
    # 写入文件
    with open(json_path, "w", encoding='utf-8') as f:
        json.dump({"agents": agents}, f, indent=4, ensure_ascii=False)
        
    return ResponseUtil.success(data=agent)

@setting_router.get("/agents")
def get_all_agents(current_user: CurrentUserDep) -> Any:
    '''
    获取所有智能体
    文件示例
    {
    "agents": [
        {
        "name": "过敏",
        "botId": "7532677049182355496",
        "isDefault": true,
        "platform": "coze",
        "id": "7532677049182355496"
        }
    ]
    }
    '''
    # 判断 agents.json 是否存在
    if not os.path.exists(os.path.join(get_base_dir(), "agents.json")):
        return ResponseUtil.success(data={"agents": []})
    
    try:
        with open(os.path.join(get_base_dir(), "agents.json"), "r", encoding='utf-8') as f:
            data = json.load(f)

    except:
        return ResponseUtil.error(msg="agents.json 格式错误")
    
    return ResponseUtil.success(data={"agents": data.get("agents", [])})


@setting_router.post("/agents")
def save_agent(current_user: CurrentUserDep, agent: dict) -> Any:
    '''
    保存智能体
    '''
    # 判断 agents.json 是否存在
    if not os.path.exists(os.path.join(get_base_dir(), "agents.json")):
        return ResponseUtil.success(data={"agents": []})
    
    try:
        with open(os.path.join(get_base_dir(), "agents.json"), "r", encoding='utf-8') as f:
            data = json.load(f)
    except:
        return ResponseUtil.error(msg="agents.json 格式错误")
    
    agents = data.get("agents", [])
    agents.append(agent)
    # 写入配置文件  
    with open(os.path.join(get_base_dir(), "agents.json"), "w", encoding='utf-8') as f:
        json.dump({"agents": agents}, f, indent=4)
    return ResponseUtil.success(data={"agents": agents})


@setting_router.put("/agents/{agent_id}/default")
def set_default_agent(current_user: CurrentUserDep, agent_id: str) -> Any:
    '''
    设置默认智能体
    '''
    if not agent_id:
        return ResponseUtil.error(msg="智能体ID不能为空")
    
    # 判断 agents.json 是否存在
    json_path = os.path.join(get_base_dir(), "agents.json")
    if not os.path.exists(json_path):
        return ResponseUtil.error(msg="配置文件不存在")
    
    try:
        with open(json_path, "r", encoding='utf-8') as f:
            data = json.load(f)
    except:
        return ResponseUtil.error(msg="agents.json 格式错误")
    
    agents = data.get("agents", [])
    found = False
    
    # 先检查ID是否存在
    for agent in agents:
        if agent.get("id") == agent_id:
            found = True
            break
            
    if not found:
        return ResponseUtil.error(msg="智能体不存在")

    # 更新状态：目标设为True，其他设为False
    for agent in agents:
        agent["isDefault"] = (agent.get("id") == agent_id)
    
    # 写入配置文件  
    with open(json_path, "w", encoding='utf-8') as f:
        json.dump({"agents": agents}, f, indent=4, ensure_ascii=False)
    
    return ResponseUtil.success()


@setting_router.delete("/agents/{agent_id}")
def del_agent(current_user: CurrentUserDep, agent_id: str) -> Any:
    '''
    删除智能体
    '''
    if not agent_id:
        return ResponseUtil.error(msg="智能体ID不能为空")
    
    # 判断 agents.json 是否存在
    if not os.path.exists(os.path.join(get_base_dir(), "agents.json")):
        return ResponseUtil.success(data={"agents": []})
    try:
        _delete_agent_by_name(agent_id=agent_id)
    except Exception as e:
        return ResponseUtil.error(msg=str(e))
    
    return ResponseUtil.success(msg="删除成功")

def _delete_agent_by_name(agent_id: str) -> bool:
    """
    内部辅助函数：根据名称删除智能体
    :param agent_id: 智能体ID
    :return: 是否删除成功（True表示有删除操作，False表示未找到）
    """
    json_path = os.path.join(get_base_dir(), "agents.json")
    try:
        with open(json_path, "r", encoding='utf-8') as f:
            data = json.load(f)
            
        agents = data.get("agents", [])
        original_count = len(agents)
        # 过滤掉匹配ID的 agent
        new_agents = [agent for agent in agents if agent.get("id") != agent_id]
        
        if len(new_agents) == original_count:
            return False # 没有找到并删除
            
        # 保存回文件
        data["agents"] = new_agents
        with open(json_path, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return data
    except Exception as e:
        logger.error(f"Error deleting agent by name: {e}")
        raise e


# 话术组管理#####################################################################################
@setting_router.get("/greeting_config")
def get_greeting_config(current_user: CurrentUserDep) -> Any:
    '''
        获取话术组配置
        文件示例:
        {
            "greeting_config": [
                {
                    "name": "A组",
                    "greetings": [
                        {
                            "type": "file",
                            "content": "huashu.txt",
                            "filePath": "data\\uploads\\greetings\\1770022528.txt"
                        },
                        {
                            "type": "text",
                            "content": "测试"
                        },
                        {
                            "type": "agent",
                            "content": "",
                            "agentId": "7532677049182355496",
                            "prompt": "请按要求生成话术"
                        }
                    ]
                }
            ]
        }
    '''
    logger.info(f"get_greeting_config: {current_user}")
    file_path = os.path.join(get_base_dir(), "greeting_config.json")
    if not os.path.exists(file_path):
        return ResponseUtil.failure(msg="greeting_config.json not found")

    try:
        with open(file_path, "r", encoding='utf-8') as f:
            data = json.load(f)
        
        config = data.get("greeting_config")
        
        # 兼容性处理：如果取出来是字典，并且里面还有 greeting_config，则继续取（处理旧的双层嵌套格式）
        if isinstance(config, dict) and "greeting_config" in config:
            config = config["greeting_config"]
            
        # 确保返回的是列表，如果不是则返回空列表
        if not isinstance(config, list):
            config = []
            
        return ResponseUtil.success(data=config)
    except Exception as e:
        # 发生错误时返回空列表，避免前端崩溃
        print(f"Error loading greeting config: {e}")
        return ResponseUtil.error(msg="Failed to load greeting config")


@setting_router.post("/greeting_config")
def save_greeting_config(current_user: CurrentUserDep, config: dict) -> Any:
    '''
    保存话术组配置
    '''
    # 前端传来的 config 已经是 {"greeting_config": [...]} 结构
    # 直接写入文件即可保持与 get_greeting_config 读取逻辑一致
    
    with open(os.path.join(get_base_dir(), "greeting_config.json"), "w", encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
        
    return ResponseUtil.success()