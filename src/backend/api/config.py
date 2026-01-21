import json
from typing import Any
from fastapi import APIRouter
import time

router = APIRouter()

@router.get("/agents")
def get_agents():
    return {"agents": ["agent1", "agent2", "agent3"]}


@router.get("/coze_settings")
def get_coze_settings():
    return {"coze_settings": {"setting1": "value1", "setting2": "value2"}}

@router.post("/coze_settings")
def set_coze_settings(settings: dict) -> Any:
    # 这里可以添加逻辑来更新Coze的设置
    # 例如，调用Coze的API来更新设置
    # 这里只是简单地返回更新后的设置
    last_update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    result = {"coze_settings": settings.get("key"), "last_update_time": last_update_time}
    # 写入配置文件  
    with open("coze_settings.json", "w") as f:
        json.dump(result, f)
        
    return "保存成功！"
