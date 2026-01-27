from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from db.get_db import get_db
from db.models import Friends, Groups, WechatAccounts

home_router = APIRouter()

@home_router.get("/init")
def init():
    return {"message": f"Welcome to the AI Bot API!"}

@home_router.get("/dashboard")
async def get_dashboard_data(db: AsyncSession = Depends(get_db)):
    # Get user info (Assuming single user or taking the first one for now)
    result = await db.execute(select(WechatAccounts).limit(1))
    user = result.scalars().first()
    
    user_name = user.nickname if user else "未登录"
    account_id = user.account_id if user else None
    
    friend_count = 0
    group_count = 0
    
    if account_id:
        # Count friends
        f_result = await db.execute(select(func.count()).select_from(Friends).where(Friends.account_id == account_id))
        friend_count = f_result.scalar()
        
        # Count groups
        g_result = await db.execute(select(func.count()).select_from(Groups).where(Groups.account_id == account_id))
        group_count = g_result.scalar()
        
    return {
        "userName": user_name,
        "friendCount": friend_count,
        "groupCount": group_count,
        "status": "在线" if user else "离线"
    }




# def task():
#     print("任务执行中...")  # 替换为你的方法
#     threading.Timer(30, task).start()  # 60秒后再次启动
#     msg = check_new_message()
#     print(msg)
#     if msg != '未查找到新消息' :
#         for m in json.loads(msg):
#             AI_auto_reply_to_friend1(m)