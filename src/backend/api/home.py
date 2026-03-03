from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.get_db import get_db
from environment import CurrentUserDep
from utils.response_util import ResponseUtil
from service.wechat_service import wechat_service
from service.friends_service import friends_service
from service.groups_service import groups_service


home_router = APIRouter()

@home_router.get("/init")
def init() -> Any:
    return ResponseUtil.success(msg="Welcome to the AI Bot API!")

@home_router.get("/dashboard")
async def get_dashboard_data(db: AsyncSession = Depends(get_db)) -> Any : 
    try:
        data = await wechat_service.get_dashboard_data(db)
        return ResponseUtil.success(
            msg=(f"当前微信号: {data['wxNumber']}, 状态: {data['status']}"),
            data=data
        )
    except Exception as e:
        # Check if error message indicates failure
        return ResponseUtil.error(msg=str(e))

@home_router.get("/friendCount")
async def get_friendCount(current_user: CurrentUserDep, db: AsyncSession = Depends(get_db)) -> Any:
    try:
        friend_count = await friends_service.get_friend_count(current_user.wxNumber, db)
        return ResponseUtil.success(
            msg="获取好友数量成功",
            data=friend_count
        )
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

@home_router.get("/groupCount")
async def get_groupCount(current_user: CurrentUserDep, db: AsyncSession = Depends(get_db)) -> Any:
    try:
        group_count = await groups_service.get_group_count(current_user.wxNumber, db)
        return ResponseUtil.success(    
            msg="获取群数量成功",
            data=group_count
        )
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

@home_router.post("/auto_configure_env")
async def auto_configure_env() -> Any:
    """
    自动配置环境：
    1. 退出微信
    2. 设置windows当前用户环境变量QT_ACCESSIBILITY=1
    3. 启动讲述人(触发Accessibility)
    4. 重启微信
    """
    try:
        await wechat_service.auto_configure_env()
        return ResponseUtil.success(msg="环境自动配置完成，微信已重启")
    except Exception as e:
        return ResponseUtil.error(msg=str(e))
