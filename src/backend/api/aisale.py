import json
import os
import time
from fastapi import APIRouter, Depends

from environment import CurrentUserDep
from utils.response_util import ResponseUtil
from utils.config_file import get_personal_dir


aisale_router = APIRouter()


# AI 助理配置（每个用户独立）
@aisale_router.get("/get_ai_config")
async def get_ai_config(current_user: CurrentUserDep):
    '''
    获取AI配置
    配置文件示例 reply_stategy.json:
    {
    "staffList": [
        {
        "id": "1772163331923",
        "name": "a",
        "enabled": true,
        "agentId": "7532677049182355496",
        "chatType": "single",
        "selectedTags": [
            "untagged"
        ],
        "keywords": []
        },
        {
        "id": "1772163960715",
        "name": "b",
        "enabled": true,
        "agentId": "7532677049182355496",
        "chatType": "single",
        "selectedTags": [
            "untagged"
        ],
        "keywords": []
        }
    ],
    "commonConfig": {
        "groupAtOnly": true,
        "colleagueNamesToIgnore": "",
        "filterWords": [
        "aa",
        "bb"
        ],
        "autoGreeting": {
        "enabled": true,
        "greetingGroupId": "A组"
        },
        "fileRecognition": {
        "enabled": true,
        "fileTypes": [
            "excel",
            "pdf"
        ],
        "filePath": "d:\\"
        },
        "whitelist": {
            "enabled": true,
            "names": "a//bb",
            "list": [
                "a",
                "bb"
            ]
            }
        }
    }
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
async def save_agent(current_user: CurrentUserDep, agent: dict):
    '''
    添加智能体
    '''
    if not isinstance(agent, dict):
        return ResponseUtil.error(msg="参数格式错误")

    name = (agent.get("name") or "").strip()
    agent_id = agent.get("agentId")
    if not name:
        return ResponseUtil.error(msg="员工名称不能为空")
    if not agent_id:
        return ResponseUtil.error(msg="智能体ID不能为空")

    chat_type = agent.get("chatType")

    selected_tags = agent.get("selectedTags")

    keywords = agent.get("keywords")
    if not isinstance(keywords, list):
        keywords = []

    enabled = agent.get("enabled")
    if enabled is None:
        enabled = False

    agent_item_id = agent.get("id")

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
    new_item = {
        "id": agent_item_id,
        "name": name,
        "enabled": bool(enabled),
        "agentId": str(agent_id),
        "chatType": chat_type,
        "selectedTags": selected_tags,
        "keywords": keywords
    }

    replaced = False
    for idx, item in enumerate(staff_list):
        if str(item.get("id")) == agent_item_id:
            staff_list[idx] = new_item
            replaced = True
            break
    if not replaced:
        staff_list.append(new_item)

    data["staffList"] = staff_list
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return ResponseUtil.error(msg=f"保存失败: {e}")

    return ResponseUtil.success(data={"staffList": staff_list})


@aisale_router.post("/delete_agent")
async def delete_agent(current_user: CurrentUserDep, agent_id: str):
    '''
    删除智能体
    '''
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
    hit_staff_id = any(str(item.get("id")) == str(agent_id) for item in staff_list)
    if hit_staff_id:
        new_staff_list = [item for item in staff_list if str(item.get("id")) != str(agent_id)]
    else:
        new_staff_list = [item for item in staff_list if str(item.get("agentId")) != str(agent_id)]
    data["staffList"] = new_staff_list
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return ResponseUtil.error(msg=f"保存失败: {e}")
    
    return ResponseUtil.success(data={"staffList": new_staff_list})
