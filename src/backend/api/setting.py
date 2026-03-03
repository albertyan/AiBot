from typing import Any
from fastapi import APIRouter
from environment import CurrentUserDep
from utils.response_util import ResponseUtil
from service.setting_service import setting_service

setting_router = APIRouter()

# AI 接入配置
@setting_router.get("/get_coze_settings")
async def get_coze_settings(current_user: CurrentUserDep) -> Any:
    '''
    获取 Coze 的 token 以及最后更新时间
    '''
    return ResponseUtil.success(data=setting_service.get_coze_settings())

@setting_router.post("/save_coze_settings")
async def set_coze_settings(current_user: CurrentUserDep, settings: dict) -> Any:
    '''
    设置 Coze 的 token
    '''
    try:
        data = setting_service.save_coze_settings(settings)
        return ResponseUtil.success(data=data)
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

@setting_router.post("/save_dify_settings")
async def save_dify_settings(current_user: CurrentUserDep, baseUrl: str) -> Any:
    '''
    设置 Dify 的地址
    '''
    try:
        data = setting_service.save_dify_settings(baseUrl)
        return ResponseUtil.success(data=data)
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

@setting_router.get("/get_dify_settings")
async def get_dify_settings(current_user: CurrentUserDep) -> Any:
    '''
    获取 Dify 的地址
    '''
    try:
        data = setting_service.get_dify_settings()
        return ResponseUtil.success(data=data)
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

# 智能体管理
@setting_router.post("/add_agents")
async def add_agent(current_user: CurrentUserDep, agent: dict) -> Any:
    '''
    添加智能体
    '''
    try:
        data = setting_service.add_agent(agent)
        return ResponseUtil.success(data=data)
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

@setting_router.get("/get_all_agents")
async def get_all_agents(current_user: CurrentUserDep) -> Any:
    '''
    获取所有智能体
    '''
    try:
        data = setting_service.get_all_agents()
        return ResponseUtil.success(data={"agents": data})
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

@setting_router.post("/save_agents")
async def save_agent(current_user: CurrentUserDep, agent: dict) -> Any:
    '''
    保存智能体
    '''
    try:
        data = setting_service.save_agent(agent)
        return ResponseUtil.success(data={"agents": data})
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

@setting_router.put("/agents/{agent_id}/default")
async def set_default_agent(current_user: CurrentUserDep, agent_id: str) -> Any:
    '''
    设置默认智能体
    '''
    try:
        setting_service.set_default_agent(agent_id)
        return ResponseUtil.success()
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

@setting_router.delete("/delete_agents/{agent_id}")
async def del_agent(current_user: CurrentUserDep, agent_id: str) -> Any:
    '''
    删除智能体
    '''
    try:
        setting_service.delete_agent(agent_id)
        return ResponseUtil.success(msg="删除成功")
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

# 话术组管理
@setting_router.get("/get_greeting_config")
async def get_greeting_config(current_user: CurrentUserDep) -> Any:
    '''
    获取话术组配置
    '''
    try:
        data = setting_service.get_greeting_config()
        return ResponseUtil.success(data=data)
    except Exception as e:
        # 发生错误时返回空列表，避免前端崩溃
        return ResponseUtil.error(msg="Failed to load greeting config")

@setting_router.post("/save_greeting_config")
async def save_greeting_config(current_user: CurrentUserDep, config: dict) -> Any:
    '''
    保存话术组配置
    '''
    try:
        setting_service.save_greeting_config(config)
        return ResponseUtil.success()
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

# 朋友圈评论
@setting_router.get("/get_moment_settings")
async def get_friend_comment_config(current_user: CurrentUserDep) -> Any:
    '''
    获取朋友圈评论配置
    '''
    try:
        data = setting_service.get_moment_settings()
        return ResponseUtil.success(data=data)
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

@setting_router.post("/save_moment_settings")
async def save_friend_comment_config(current_user: CurrentUserDep, config: dict) -> Any:
    '''
    保存朋友圈评论配置
    '''
    try:
        setting_service.save_moment_settings(config)
        return ResponseUtil.success()
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

# AI回复配置
@setting_router.get("/get_chat_history_settings")
async def get_ai_reply_config(current_user: CurrentUserDep) -> Any:
    '''
    获取AI回复配置
    '''
    try:
        data = setting_service.get_chat_history_settings()
        return ResponseUtil.success(data=data)
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

@setting_router.post("/save_chat_history_settings")
async def save_ai_reply_config(current_user: CurrentUserDep, config: dict) -> Any:
    '''
    保存AI回复配置
    '''
    try:
        setting_service.save_chat_history_settings(config)
        return ResponseUtil.success()
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

# 预警配置
@setting_router.get("/get_alert_settings")
async def get_alert_config(current_user: CurrentUserDep) -> Any:
    '''
    获取预警配置
    '''
    try:
        data = setting_service.get_alert_settings()
        return ResponseUtil.success(data=data)
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

@setting_router.post("/save_alert_settings")
async def save_alert_config(current_user: CurrentUserDep, config: dict) -> Any:
    '''
    保存预警配置
    '''
    try:
        setting_service.save_alert_settings(config)
        return ResponseUtil.success()
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

@setting_router.post("/test_alert_email")
async def send_test_alert_email(email: str) -> Any: 
    '''
    发送测试预警邮件
    '''
    try:
        setting_service.send_test_alert_email(email)
        return ResponseUtil.success(msg="发送邮件成功")
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

# 休息时间设置
@setting_router.get("/get_rest_time_settings")
async def get_rest_time_config(current_user: CurrentUserDep) -> Any:
    '''
    获取休息时间配置
    '''
    try:
        data = setting_service.get_rest_time_settings()
        return ResponseUtil.success(data=data)
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

@setting_router.post("/save_rest_time_settings")
async def save_rest_time_config(current_user: CurrentUserDep, config: dict) -> Any:
    '''
    保存休息时间配置
    '''
    try:
        setting_service.save_rest_time_settings(config)
        return ResponseUtil.success()
    except Exception as e:
        return ResponseUtil.error(msg=str(e))
