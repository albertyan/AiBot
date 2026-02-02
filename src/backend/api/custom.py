from typing import Any
from loguru import logger
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, func, distinct, update

from db.get_db import get_db
from auto.WeChatAutoExt import ContactsExt
from db.models import Friends, Groups, Message, ContactTags
from environment import state, current_user

custom_router = APIRouter()

@custom_router.get("/sync_friend")
async def sync_friend(db: AsyncSession = Depends(get_db)) -> Any:
    '''
    同步好友列表
    '''
    # info={'昵称':nickname,'微信号':wx_number,'地区':region,'备注':remark,'电话':phonenumber,
    # '标签':tag,'描述':descrption,'朋友权限':permission,'共同群聊':f'{common_group_num}','个性签名':signature,'来源':source}
    # 同步好友列表

    current_user = state.get_current_user()
    if not current_user:
        return Message(code=400, message="当前用户不存在")
    # 删除当前用户的好友列表
    stmt = delete(Friends).where(Friends.account_id == current_user.wxNumber)
    await db.execute(stmt)
    # 提交事务
    await db.commit()
    friends = ContactsExt.get_friends_detail()
    tag_counts = {}
    for friend in friends:
        # 统计标签
        tag_str = friend.get('标签', '')
        if tag_str:
            # 替换中文逗号
            tag_str = tag_str.replace('，', ',')
            tags = [t.strip() for t in tag_str.split(',') if t.strip()]
            for tag in tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # 如果不存在，则创建新记录
        new_friend = Friends(account_id=current_user.wxNumber,
                             wxid=friend['微信号'],
                             remark=friend['备注'],
                             tag=friend['标签'],
                             nickname=friend['昵称'],
                             name=friend['昵称'],
                             region=friend['地区'],
                             permission=friend['朋友权限'],
                             phonenumber=friend['电话'],
                             description=friend['描述'],
                             source=friend['来源'],
                             signature=friend['个性签名'],
                             is_new=0,
                             create_time=func.now(),
                             update_time=func.now(),
                             del_flag=0)
        db.add(new_friend)
    # 提交事务
    await db.commit()
    # 删除当前用户的标签列表
    stmt = delete(ContactTags).where(ContactTags.account_id == current_user.wxNumber)
    await db.execute(stmt)
    # 提交事务
    await db.commit()
    # 插入标签统计
    for tag, count in tag_counts.items():
        # 如果不存在，则创建新记录
        new_tag = ContactTags(account_id=current_user.wxNumber,
                             tag=tag,
                             contact_count=count,
                             create_time=func.now(),
                             update_time=func.now(),
                             del_flag=0)
        db.add(new_tag)
    # 提交事务
    await db.commit()

    return Message(code=200, message="好友列表同步完成", data={'friends': friends, 'tags': list(tag_counts.keys())})

@custom_router.get("/sync_group", response_model=Message)
async def sync_group(db: AsyncSession = Depends(get_db)) -> Any:
    '''
    同步群聊列表
    '''
    # 同步群聊列表
    current_user = state.get_current_user()
    if not current_user:
        return Message(code=400, message="当前用户不存在")
    # 删除当前用户的群聊列表
    stmt = delete(Groups).where(Groups.account_id == current_user.wxNumber)
    await db.execute(stmt)
    # 提交事务
    await db.commit()
    groups = ContactsExt.get_recent_groups()
    processed_groups = set()
    for group in groups:
        group_name = group[0]
        if group_name in processed_groups:
            continue
        processed_groups.add(group_name)
        
        # 如果不存在，则创建新记录
        new_group = Groups(account_id=current_user.wxNumber,
                             name=group_name,
                             tag='group',
                             create_time=func.now(),
                             update_time=func.now(),
                             del_flag=0)
        db.add(new_group)
    # 提交事务
    await db.commit()
    return Message(code=200, message="群聊列表同步完成", data={'groups': groups, 'tags': list('group')})


@custom_router.get("/friends", response_model=Message)
async def get_all_friends(db: AsyncSession = Depends(get_db)) -> Any:
    '''
    获取所有好友
    '''
    current_user = state.get_current_user()
    if not current_user:
        return Message(code=400, message="当前用户不存在")
    # 查询所有好友
    stmt = select(Friends).where(Friends.account_id == current_user.wxNumber, Friends.del_flag == 0)
    result = await db.execute(stmt)
    friends = result.scalars().all()
    friends = [f.to_dict() for f in friends]
    return Message(code=200, message="好友列表查询完成", data=friends)


@custom_router.get("/groups")
async def get_all_groups(db: AsyncSession = Depends(get_db)) -> Message:
    '''
    获取所有群聊
    '''
    current_user = state.get_current_user()
    if not current_user:
        return Message(code=400, message="当前用户不存在")
    # 查询所有群聊
    stmt = select(Groups).where(Groups.account_id == current_user.wxNumber, Groups.del_flag == 0)
    result = await db.execute(stmt)
    groups = result.scalars().all()
    groups = [g.to_dict() for g in groups]
    return Message(code=200, message="群聊列表查询完成", data=groups)


@custom_router.get("/friend_tags")
async def get_all_friend_tags(db: AsyncSession = Depends(get_db)) -> Message:
    '''
    获取所有好友标签
    '''
    current_user = state.get_current_user()
    if not current_user:
        return Message(code=400, message="当前用户不存在")
    # 查询所有好友标签
    stmt = select(ContactTags).where(ContactTags.account_id == current_user.wxNumber, ContactTags.tag != 'group', ContactTags.del_flag == 0)
    result = await db.execute(stmt)
    tags = result.scalars().all()
    tags = [t.to_dict() for t in tags]
    return Message(code=200, message="好友标签查询完成", data=tags)


@custom_router.get("/group_tags", response_model=Message)
async def get_all_group_tags(db: AsyncSession = Depends(get_db)) -> Any:
    '''
    获取所有群聊标签
    '''
    current_user = state.get_current_user()
    if not current_user:
        return Message(code=400, message="当前用户不存在")
    # 查询所有群聊标签
    stmt = select(distinct(Groups.tag)).where(Groups.account_id == current_user.wxNumber, Groups.del_flag == 0)
    result = await db.execute(stmt)
    tags = result.scalars().all()
    # 过滤空标签
    tags = [t for t in tags if t]
    return Message(code=200, message="群聊标签查询完成", data=tags)

@custom_router.post("/set_group_tags", response_model=Message)
async def set_group_tags(groups: list[str], tag: str, db: AsyncSession = Depends(get_db)) -> Any:
    '''
    设置群聊标签
    '''
    current_user = state.get_current_user()
    if not current_user:
        return Message(code=400, message="当前用户不存在")
    # 设置群聊标签
    for group in groups:
        stmt = update(Groups).where(Groups.account_id == current_user.wxNumber, Groups.name == group).values(tag=tag)
        await db.execute(stmt)
    # 提交事务
    await db.commit()
    return Message(code=200, message="群聊标签设置完成")