class EnvMode:
    DEV = "dev"
    PROD = "prod"
    def __init__(self):
        self.envMode = self.DEV
    
    def set_mode(self, mode: str):
        self.envMode = mode

env = EnvMode()

class GlobalState:
    """
    维护后端全局状态的简单容器
    选择后端内存全局存储而不是请求上下文，原因是当前项目仅运行在单进程桌面应用内，
    不涉及多实例/分布式，使用内存即可满足“跨接口共享当前用户”的需求
    """
    def __init__(self):
        # 使用字典而非 ORM 实例，原因是 ORM 对象关联会话生命周期，跨请求持有可能导致意外引用和线程安全问题
        self.current_user: dict | None = None

    def set_current_user(self, user: dict | None):
        # 明确设置全局当前用户，避免隐式依赖请求上下文
        self.current_user = user

    def get_current_user(self) -> dict | None:
        # 读取当前用户，供路由或服务层使用
        return self.current_user

state = GlobalState()

if __name__ == "__main__":
    # env = EnvMode()
    print(f"Current environment mode: {env.envMode}")
    # Example of setting the mode
    env.set_mode(EnvMode.PROD)
    print(f"Updated environment mode: {env.envMode}")
