from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.get_db import get_db
from utils.response_util import ResponseUtil
from environment import CurrentUserDep
from service.friends_service import friends_service
from service.groups_service import groups_service

custom_router = APIRouter()

@custom_router.get("/current_user")
async def get_current_user(current_user: CurrentUserDep) -> Any:
    '''
    获取当前用户信息
    '''
    return ResponseUtil.success(data=current_user)

@custom_router.get("/sync_friend")
async def sync_friend(wx_number: str, db: AsyncSession = Depends(get_db)) -> Any:
    '''
    同步好友列表
    # info={'昵称':nickname,'微信号':wx_number,'地区':region,'备注':remark,'电话':phonenumber,
    # '标签':tag,'描述':descrption,'朋友权限':permission,'共同群聊':f'{common_group_num}','个性签名':signature,'来源':source}
    # 同步好友列表
    '''
    try:
        data = await friends_service.sync_friends(wx_number, db)
        return ResponseUtil.success(msg="好友列表同步完成", data=data)
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

@custom_router.get("/sync_group")
async def sync_group(wx_number: str, db: AsyncSession = Depends(get_db)) -> Any:
    '''
    同步群聊列表
    '''
    try:
        data = await groups_service.sync_groups(wx_number, db)
        return ResponseUtil.success(msg="群聊列表同步完成", data=data)
    except Exception as e:
        return ResponseUtil.error(msg=str(e))


@custom_router.get("/friends")
async def get_all_friends(wx_number: str, db: AsyncSession = Depends(get_db)) -> Any:
    '''
    获取所有好友
    '''
    try:
        data = await friends_service.get_all_friends(wx_number, db)
        return ResponseUtil.success(msg="好友列表查询完成", data=data)
    except Exception as e:
        return ResponseUtil.error(msg=str(e))


@custom_router.get("/groups")
async def get_all_groups(wx_number: str, db: AsyncSession = Depends(get_db)) -> Any:
    '''
    获取所有群聊
    '''
    try:
        data = await groups_service.get_all_groups(wx_number, db)
        return ResponseUtil.success(msg="群聊列表查询完成", data=data)
    except Exception as e:
        return ResponseUtil.error(msg=str(e))


@custom_router.get("/friend_tags")
async def get_all_friend_tags(wx_number: str, db: AsyncSession = Depends(get_db)) -> Any:
    '''
    获取所有好友标签
    '''
    try:
        data = await friends_service.get_all_friend_tags(wx_number, db)
        return ResponseUtil.success(msg="好友标签查询完成", data=data)
    except Exception as e:
        return ResponseUtil.error(msg=str(e))


@custom_router.get("/group_tags")
async def get_all_group_tags(wx_number: str,  db: AsyncSession = Depends(get_db)) -> Any:
    '''
    获取所有群聊标签
    '''
    try:
        data = await groups_service.get_all_group_tags(wx_number, db)
        return ResponseUtil.success(msg="群聊标签查询完成", data=data)
    except Exception as e:
        return ResponseUtil.error(msg=str(e))

@custom_router.post("/set_group_tags")
async def set_group_tags(wx_number: str, groups: list[str], tag: str, db: AsyncSession = Depends(get_db)) -> Any:
    '''
    设置群聊标签
    '''
    try:
        await groups_service.set_group_tags(wx_number, groups, tag, db)
        return ResponseUtil.success(msg="群聊标签设置完成")
    except Exception as e:
        return ResponseUtil.error(msg=str(e))
