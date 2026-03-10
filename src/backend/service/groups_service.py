from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, func, distinct, update
from auto.WeChatAutoExt import ContactsExt
from db.models import Groups
from utils.perf_util import instrument_class
from environment import state
from loguru import logger

class GroupsService:
    def __init__(self):
        pass

    async def sync_groups(self, wx_number: str, db: AsyncSession) -> Dict[str, Any]:
        """
        同步群聊列表
        """
        # 删除当前用户的群聊列表
        stmt = delete(Groups).where(Groups.account_id == wx_number)
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
            new_group = Groups(account_id=wx_number,
                                 name=group_name,
                                 tag='group',
                                 create_time=func.now(),
                                 update_time=func.now(),
                                 del_flag=0)
            db.add(new_group)
        # 提交事务
        await db.commit()
        
        # 更新全局缓存
        try:
            all_groups = await self.get_all_groups(wx_number, db)
            state.set_groups(wx_number, all_groups)
        except Exception as e:
            logger.error(f"更新群聊缓存失败: {e}")

        return {'groups': groups, 'tags': list('group')}

    async def get_all_groups(self, wx_number: str, db: AsyncSession) -> List[Dict[str, Any]]:
        """
        获取所有群聊
        """
        stmt = select(Groups).where(Groups.account_id == wx_number, Groups.del_flag == 0)
        result = await db.execute(stmt)
        groups = result.scalars().all()
        return [g.to_dict() for g in groups]

    async def get_all_group_tags(self, wx_number: str, db: AsyncSession) -> List[str]:
        """
        获取所有群聊标签
        """
        stmt = select(distinct(Groups.tag)).where(Groups.account_id == wx_number, Groups.del_flag == 0)
        result = await db.execute(stmt)
        tags = result.scalars().all()
        # 过滤空标签
        return [t for t in tags if t]

    async def set_group_tags(self, wx_number: str, groups: List[str], tag: str, db: AsyncSession):
        """
        设置群聊标签
        """
        for group in groups:
            stmt = update(Groups).where(Groups.account_id == wx_number, Groups.name == group).values(tag=tag)
            await db.execute(stmt)
        # 提交事务
        await db.commit()

    async def get_group_count(self, wx_number: str, db: AsyncSession) -> int:
        """
        获取群数量
        """
        result = await db.execute(select(func.count(Groups.id)).where(Groups.account_id == wx_number))
        return result.scalar()

GroupsService = instrument_class(GroupsService, prefix="service.GroupsService")
groups_service = GroupsService()
