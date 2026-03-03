from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, func
from loguru import logger
import pandas as pd
import io

from auto.WeChatAutoExt import ContactsExt
from db.models import Friends, ContactTags
from utils.perf_util import instrument_class

class FriendsService:
    def __init__(self):
        pass

    async def sync_friends(self, wx_number: str, db: AsyncSession) -> Dict[str, Any]:
        """
        同步好友列表
        """
        # 删除当前用户的好友列表
        stmt = delete(Friends).where(Friends.account_id == wx_number)
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
            new_friend = Friends(account_id=wx_number, wxid=friend['微信号'],
                                 remark=friend['备注'], tag=friend['标签'],
                                 nickname=friend['昵称'], name=friend['昵称'],
                                 region=friend['地区'], permission=friend['朋友权限'],
                                 phonenumber=friend['电话'], description=friend['描述'],
                                 source=friend['来源'], signature=friend['个性签名'], is_new=0,
                                 create_time=func.now(), update_time=func.now(), del_flag=0)
            db.add(new_friend)
        # 提交事务
        await db.commit()
        
        # 删除当前用户的标签列表
        stmt = delete(ContactTags).where(ContactTags.account_id == wx_number)
        await db.execute(stmt)
        # 提交事务
        await db.commit()
        
        # 插入标签统计
        for tag, count in tag_counts.items():
            # 如果不存在，则创建新记录
            new_tag = ContactTags(account_id=wx_number,
                                 tag=tag,
                                 contact_count=count,
                                 create_time=func.now(),
                                 update_time=func.now(),
                                 del_flag=0)
            db.add(new_tag)
        # 提交事务
        await db.commit()
        
        return {'friends': friends, 'tags': list(tag_counts.keys())}

    async def get_all_friends(self, wx_number: str, db: AsyncSession) -> List[Dict[str, Any]]:
        """
        获取所有好友
        """
        stmt = select(Friends).where(Friends.account_id == wx_number, Friends.del_flag == 0)
        result = await db.execute(stmt)
        friends = result.scalars().all()
        return [f.to_dict() for f in friends]

    async def get_all_friend_tags(self, wx_number: str, db: AsyncSession) -> List[Dict[str, Any]]:
        """
        获取所有好友标签
        """
        stmt = select(ContactTags).where(ContactTags.account_id == wx_number, ContactTags.tag != 'group', ContactTags.del_flag == 0)
        result = await db.execute(stmt)
        tags = result.scalars().all()
        return [t.to_dict() for t in tags]

    async def get_friend_count(self, wx_number: str, db: AsyncSession) -> int:
        """
        获取好友数量
        """
        result = await db.execute(select(func.count(Friends.id)).where(Friends.account_id == wx_number))
        return result.scalar()

    def parse_friend_list_file(self, content: bytes, filename: str) -> List[Dict[str, str]]:
        """
        解析好友名单文件
        """
        df = None
        # 显式关闭头部推断（header=None），避免 pandas 将首行直接当作列名
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            df = pd.read_excel(io.BytesIO(content), header=None)
        elif filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content), header=None)
        else:
            raise ValueError("不支持的文件格式")

        if df is None:
             raise ValueError("文件读取失败")
             
        # 确保至少有3列
        if len(df.columns) < 3:
            raise ValueError("文件格式错误，至少需要3列（微信号/手机号，备注，标签）")

        # 首行是否为标题的判断逻辑
        def is_header_row(row_vals):
            header_keywords = ['微信号', '帐号', '账号', '手机号', '手机', '备注', '标签', '昵称']
            for v in row_vals:
                s = str(v).strip().lower()
                if not s:
                    continue
                # 命中常见中文字段或包含“号/名/标签”等明显非数据词
                if any(k in s for k in header_keywords):
                    return True
            return False

        start_idx = 0
        if df.shape[0] > 0:
            first_row_vals = df.iloc[0, :3].tolist()
            if is_header_row(first_row_vals):
                start_idx = 1  # 跳过标题行

        # 提取数据：前三列分别映射为 account / remark / tags
        data = []
        for _, row in df.iloc[start_idx:, :3].iterrows():
            # 处理 NaN 值
            item = {
                "account": str(row[0]) if pd.notna(row[0]) else "",
                "remark": str(row[1]) if pd.notna(row[1]) else "",
                "tags": str(row[2]) if pd.notna(row[2]) else ""
            }
            # 过滤掉账号为空的行
            if item["account"].strip():
                data.append(item)
                
        return data

FriendsService = instrument_class(FriendsService, prefix="service.FriendsService")
friends_service = FriendsService()
