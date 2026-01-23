from sqlalchemy import Column, Integer, Text, String, BigInteger, DateTime, ForeignKey, UniqueConstraint, Boolean, Float, LargeBinary
# from sqlalchemy.ext.declarative import declarative_base
from db.database import Base, BaseMixin
from sqlalchemy.orm import sessionmaker

# --- Generated Models ---

# Generated from contacts.sql
class Contacts(BaseMixin, Base):
    __tablename__ = 'contacts'
    __table_args__ = (
        UniqueConstraint('account_id', 'name', 'tag', 'type'),
        {'sqlite_autoincrement': True}
    )

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False) # 显式定义以确保在第一列
    account_id = Column(Text, ForeignKey('wechat_accounts.account_id'))
    name = Column(Text, nullable=False)
    tag = Column(Text)
    type = Column(Text)

# Generated from contact_tags.sql
class ContactTags(BaseMixin, Base):
    __tablename__ = 'contact_tags'
    __table_args__ = (
        UniqueConstraint('account_id', 'tag_name'),
        {'sqlite_autoincrement': True}
    )

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False) # 显式定义以确保在第一列
    account_id = Column(Text, ForeignKey('wechat_accounts.account_id'), nullable=False)
    tag_name = Column(Text, nullable=False)
    contact_count = Column(Integer, default=0)

# Generated from friends.sql
class Friends(BaseMixin, Base):
    __tablename__ = 'friends'
    __table_args__ = (
        UniqueConstraint('account_id', 'wxid', 'tag'),
        {'sqlite_autoincrement': True}
    )

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False) # 显式定义以确保在第一列
    account_id = Column(Text, ForeignKey('wechat_accounts.account_id'), nullable=False)
    wxid = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    nickname = Column(Text)
    remark = Column(Text)
    tag = Column(Text)
    is_new = Column(Integer, default=0)


# Generated from friend_list.sql
class FriendList(BaseMixin, Base):
    __tablename__ = 'friend_list'
    __table_args__ = (
        UniqueConstraint('wxid'),
        {'sqlite_autoincrement': True}
    )

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False) # 显式定义以确保在第一列
    wxid = Column(Text, nullable=False)
    remark = Column(Text)
    tags = Column(Text)
    nickname = Column(Text)
    status = Column(Text, default='pending')
    error = Column(Text)
    account_id = Column(Text)

# Generated from groups.sql
class Groups(BaseMixin, Base):
    __tablename__ = 'groups'
    __table_args__ = (
        UniqueConstraint('account_id', 'name'),
        {'sqlite_autoincrement': True}
    )

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False) # 显式定义以确保在第一列
    account_id = Column(Text, ForeignKey('wechat_accounts.account_id'), nullable=False)
    name = Column(Text, nullable=False)
    tag = Column(Text, default='')


# Generated from group_members.sql
class GroupMembers(BaseMixin, Base):
    __tablename__ = 'group_members'
    __table_args__ = (
        UniqueConstraint('group_name', 'nickname'),
        {'sqlite_autoincrement': True}
    )

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False) # 显式定义以确保在第一列
    group_name = Column(Text, nullable=False)
    nickname = Column(Text, nullable=False)
    gender = Column(Text)
    wx_id = Column(Text)
    region = Column(Text)
    is_friend = Column(Integer, default=0)

# Generated from wechat_accounts.sql
class WechatAccounts(BaseMixin, Base):
    __tablename__ = 'wechat_accounts'
    __table_args__ = (
        UniqueConstraint('account_id'),
        UniqueConstraint('nickname', 'account_id'),
        {'sqlite_autoincrement': True}
    )

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False) # 显式定义以确保在第一列
    nickname = Column(Text, nullable=False)
    account_id = Column(Text)
