from typing import Annotated

from fastapi import Depends, HTTPException
from loguru import logger


class EnvMode:
    DEV = "dev"
    PROD = "prod"
    def __init__(self):
        self.envMode = self.DEV
    
    def set_mode(self, mode: str):
        self.envMode = mode

env = EnvMode()

class CurrentUser:
    """
    当前登录用户的全局状态容器
    """
    wxNickname : str
    wxNumber : str
    def __init__(self, nickname: str = "", number: str = ""):
        self.wxNickname = nickname
        self.wxNumber = number
import time

class GlobalState:
    """
    维护后端全局状态的简单容器
    选择后端内存全局存储而不是请求上下文，原因是当前项目仅运行在单进程桌面应用内，
    不涉及多实例/分布式，使用内存即可满足“跨接口共享当前用户”的需求
    """
    # 缓存超时时间（7天）
    CACHE_TIMEOUT_SECONDS = 7 * 24 * 60 * 60

    def __init__(self):
        # 使用字典而非 ORM 实例，原因是 ORM 对象关联会话生命周期，跨请求持有可能导致意外引用和线程安全问题
        self.current_user: CurrentUser | None = None
        # 全局缓存好友和群列表 {wx_number: [item1, item2]}
        self.friends: dict[str, list[dict]] = {}
        self.groups: dict[str, list[dict]] = {}
        # 记录缓存更新时间 {wx_number: timestamp}
        self.friends_update_time: dict[str, float] = {}
        self.groups_update_time: dict[str, float] = {}

    def set_current_user(self, user: CurrentUser | None):
        # 明确设置全局当前用户，避免隐式依赖请求上下文
        self.current_user = user

    def get_current_user(self) -> CurrentUser | None:
        # 读取当前用户，供路由或服务层使用
        return self.current_user

    def set_friends(self, wx_number: str, friends: list[dict]):
        """更新指定微信号的好友缓存"""
        self.friends[wx_number] = friends
        self.friends_update_time[wx_number] = time.time()

    def get_friends(self, wx_number: str) -> list[dict]:
        """获取指定微信号的好友缓存"""
        if wx_number in self.friends_update_time:
            if time.time() - self.friends_update_time[wx_number] > self.CACHE_TIMEOUT_SECONDS:
                raise TimeoutError(f"Friends cache for {wx_number} has expired (limit: 7 days)")
        return self.friends.get(wx_number, [])

    def set_groups(self, wx_number: str, groups: list[dict]):
        """更新指定微信号的群聊缓存"""
        self.groups[wx_number] = groups
        self.groups_update_time[wx_number] = time.time()

    def get_groups(self, wx_number: str) -> list[dict]:
        """获取指定微信号的群聊缓存"""
        if wx_number in self.groups_update_time:
            if time.time() - self.groups_update_time[wx_number] > self.CACHE_TIMEOUT_SECONDS:
                raise TimeoutError(f"Groups cache for {wx_number} has expired (limit: 7 days)")
        return self.groups.get(wx_number, [])

state = GlobalState()

def get_current_user() -> CurrentUser:
    """
    获取当前登录用户
    """
    user = state.get_current_user()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.wxNumber:
        raise HTTPException(status_code=400, detail="Not Invaild User")
    logger.info(f"get_current_user: {user.wxNumber}")
    return user

CurrentUserDep = Annotated[CurrentUser, Depends(get_current_user)]

if __name__ == "__main__":
    # env = EnvMode()
    print(f"Current environment mode: {env.envMode}")
    # Example of setting the mode
    env.set_mode(EnvMode.PROD)
    print(f"Updated environment mode: {env.envMode}")
