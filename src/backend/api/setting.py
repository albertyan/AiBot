import json
import math
import os
from typing import Any
from fastapi import APIRouter
import time
from db.models import Message

from utils.config_file import get_base_dir

setting_router = APIRouter()

@setting_router.get("/agents")
def get_agents():
    return {"agents": ["agent1", "agent2", "agent3"]}


@setting_router.get("/coze_settings")
def get_coze_settings() -> Message:
    with open(os.path.join(get_base_dir(), "coze_settings.json"), "r", encoding='utf-8') as f:
        data = json.load(f)
    last_update_time = data.get("last_update_time")

    # 计算last_update_time 距离当前时间的天数
    last_update_time_seconds = time.mktime(time.strptime(last_update_time, "%Y-%m-%d %H:%M:%S"))
    current_time_seconds = time.time()
    seconds_since_last_update = current_time_seconds - last_update_time_seconds
    # 转换为天数, 向上取整
    days_since_last_update = math.ceil(seconds_since_last_update / (24 * 60 * 60))
    return Message(code=200,message="success",
                   data={"data": data.get("coze_settings"), 
                         "tokenLastUpdated": days_since_last_update})

@setting_router.post("/coze_settings")
def set_coze_settings(settings: dict) -> Any:
    # 这里可以添加逻辑来更新Coze的设置
    # 例如，调用Coze的API来更新设置
    # 这里只是简单地返回更新后的设置
    last_update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    result = {"coze_settings": {"token": settings.get("token"), "tokenLastUpdated": last_update_time}}
    
    # 写入配置文件  
    with open(os.path.join(get_base_dir(), "coze_settings.json"), "w", encoding='utf-8') as f:
        json.dump(result, f, indent=4)
        
    return Message(code=200,message="success",data=result)


@setting_router.get("/greeting_config")
def get_greeting_config() -> Message:
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
    file_path = os.path.join(get_base_dir(), "greeting_config.json")
    if not os.path.exists(file_path):
        return Message(code=200, message="success", data=[])

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
            
        return Message(code=200, message="success", data=config)
    except Exception as e:
        # 发生错误时返回空列表，避免前端崩溃
        print(f"Error loading greeting config: {e}")
        return Message(code=200, message="success", data=[])


@setting_router.post("/greeting_config")
def save_greeting_config(config: dict) -> Message:
    '''
    保存话术组配置
    '''
    # 前端传来的 config 已经是 {"greeting_config": [...]} 结构
    # 直接写入文件即可保持与 get_greeting_config 读取逻辑一致
    
    with open(os.path.join(get_base_dir(), "greeting_config.json"), "w", encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
        
    return Message(code=200, message="success")
