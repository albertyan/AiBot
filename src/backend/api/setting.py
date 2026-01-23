import json
import math
import os
from typing import Any
from fastapi import APIRouter
import time

from utils.config_file import get_base_dir

setting_router = APIRouter()

@setting_router.get("/agents")
def get_agents():
    return {"agents": ["agent1", "agent2", "agent3"]}


@setting_router.get("/coze_settings")
def get_coze_settings():
    with open(os.path.join(get_base_dir(), "coze_settings.json"), "r") as f:
        data = json.load(f)
    last_update_time = data.get("last_update_time")

    # 计算last_update_time 距离当前时间的天数
    last_update_time_seconds = time.mktime(time.strptime(last_update_time, "%Y-%m-%d %H:%M:%S"))
    current_time_seconds = time.time()
    seconds_since_last_update = current_time_seconds - last_update_time_seconds
    # 转换为天数, 向上取整
    days_since_last_update = math.ceil(seconds_since_last_update / (24 * 60 * 60))
    return {"coze_settings": {"data": data.get("coze_settings"), "tokenLastUpdated": days_since_last_update}}

@setting_router.post("/coze_settings")
def set_coze_settings(settings: dict) -> Any:
    # 这里可以添加逻辑来更新Coze的设置
    # 例如，调用Coze的API来更新设置
    # 这里只是简单地返回更新后的设置
    last_update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    result = {"coze_settings": {"token": settings.get("token"), "tokenLastUpdated": last_update_time}}
    
    # 写入配置文件  
    with open(os.path.join(get_base_dir(), "coze_settings.json"), "w") as f:
        json.dump(result, f, indent=4)
        
    return "保存成功！"
