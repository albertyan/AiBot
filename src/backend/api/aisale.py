from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from db.get_db import get_db

from environment import CurrentUserDep
from utils.response_util import ResponseUtil
from .schemas import CommonConfig, StaffAgent, AgentId, UpdateEnableStatus, MonitorControl, WeChatSession

from service.ai_config_service import ai_config_service
from service.monitor_service import monitor_service
from service.wechat_service import wechat_service
from service.groups_service import groups_service

aisale_router = APIRouter()


# AI 助理配置（每个用户独立）
@aisale_router.get("/get_ai_config")
async def get_ai_config(current_user: CurrentUserDep):
    '''
    获取AI配置
    配置文件示例 reply_stategy.json
    '''
    try:
        data = ai_config_service.get_ai_config(current_user.wxNumber)
        return ResponseUtil.success(data={"config": data})
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

@aisale_router.post("/save_agent")
async def save_agent(current_user: CurrentUserDep, agent: StaffAgent):
    '''
    添加智能体
    '''
    try:
        staff_list = ai_config_service.save_agent(current_user.wxNumber, agent)
        return ResponseUtil.success(data={"staffList": staff_list})
    except Exception as e:
        return ResponseUtil.error(msg=str(e))


@aisale_router.post("/delete_agent")
async def delete_agent(current_user: CurrentUserDep, data_in: AgentId):
    '''
    删除智能体
    '''
    if not data_in.agent_id:
        return ResponseUtil.error(msg="智能体ID不能为空")
    
    try:
        new_staff_list = ai_config_service.delete_agent(current_user.wxNumber, data_in.agent_id)
        return ResponseUtil.success(data={"staffList": new_staff_list})
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

@aisale_router.post("/save_common_config")
async def save_common_config(current_user: CurrentUserDep, config: CommonConfig):
    '''
    保存通用配置
    '''
    try:
        common_config = ai_config_service.save_common_config(current_user.wxNumber, config)
        return ResponseUtil.success(data={"commonConfig": common_config})
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

@aisale_router.post("/update_enable_status")
async def update_enable_status(current_user: CurrentUserDep, status: UpdateEnableStatus):
    '''
    更新启用状态
    '''
    try:
        ai_config_service.update_enable_status(current_user.wxNumber, status.agent_id, status.enabled)
        return ResponseUtil.success()
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

@aisale_router.post("/refresh_weixin_messages")
async def refresh_weixin_messages(current_user: CurrentUserDep, db: AsyncSession = Depends(get_db)):
    '''
    刷新微信消息
    Return:返回新消息列表
    '''
    try:
        groups = await groups_service.get_all_groups(current_user.wxNumber, db)
        group_names = [g.get('name') for g in groups]
        sessions = wechat_service.get_new_messages(current_user.wxNumber)
        for s in sessions:
            if s.name in group_names:
                s.is_group = True
        return ResponseUtil.success(data={"sessions": [s.model_dump() for s in sessions]})
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

@aisale_router.get("/pull_friend_messages")
async def pull_friend_messages(current_user: CurrentUserDep, db: AsyncSession = Depends(get_db),is_group:bool=False, friend:str=""):
    '''
    获取单个微信会话列表
    '''
    try:

        logger.info(f"current_user.wxNumber: {current_user.wxNumber}")
        sessions = wechat_service.pull_friend_messages(current_user.wxNumber, friend)
        return ResponseUtil.success(data={"sessions": sessions})
    except Exception as e:
        return ResponseUtil.error(msg=str(e))


@aisale_router.post("/toggle_monitor")
async def toggle_monitor(current_user: CurrentUserDep, data: MonitorControl):
    """
    开启或关闭微信消息监控
    """
    try:
        if data.enabled:
            monitor_service.start_monitor()
            msg = "监控已启动"
        else:
            monitor_service.stop_monitor()
            msg = "监控已停止"
        
        return ResponseUtil.success(msg=msg)
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

@aisale_router.get("/get_monitor_status")
async def get_monitor_status(current_user: CurrentUserDep):
    """
    获取微信消息监控状态
    """
    try:
        status = monitor_service.get_monitor_status()
        return ResponseUtil.success(data={"enabled": status})
    except Exception as e:
        return ResponseUtil.error(msg=str(e))


