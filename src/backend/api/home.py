from fastapi import APIRouter


from data.sqliteDB import SQLiteDB
import threading
import json



router = APIRouter()

@router.get("/init")
def init():

    try:
        db = SQLiteDB("wechat_contacts.db")
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return {"error": "数据库连接失败"}
    
    return {"message": f"Welcome to the AI Bot API!"}




# def task():
#     print("任务执行中...")  # 替换为你的方法
#     threading.Timer(30, task).start()  # 60秒后再次启动
#     msg = check_new_message()
#     print(msg)
#     if msg != '未查找到新消息' :
#         for m in json.loads(msg):
#             AI_auto_reply_to_friend1(m)