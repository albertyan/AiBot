''' -*- coding: utf-8 -*-
# @Author  : Ficus
# @Time    : 2024/11/4 15:14
# @File    : server.py
'''
import os

from fastapi import APIRouter, WebSocket
from fastapi.responses import FileResponse, HTMLResponse
from loguru import logger
from environment import env, EnvMode
import importlib.util
from config.env import *

router = APIRouter()

# if env.envMode == EnvMode.DEV:
#     from src import baseUtil
# else:
#     import baseUtil

BASE_DIR = os.path.abspath(os.getcwd())

dist_dir = os.path.join(BASE_DIR, "dist", "gui")

@router.get("/", response_class=HTMLResponse)
def hello():
    """
    使用 UTF-8 编码读取前端构建后的首页 HTML，避免在中文环境下因系统默认编码为 GBK 导致解析失败
    """
    indexpath = os.path.join(dist_dir, "index.html")
    logger.info(indexpath)
    logger.info(settingFileConfig.COZE_SETTINGS_FILE)
    # 指定 UTF-8 编码读取文件，避免 Windows 默认 GBK 解码失败
    with open(indexpath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


@router.websocket("/")
async def websocket_root(websocket: WebSocket):
    """
    提供一个与浏览器默认尝试访问路径一致的 We日志干扰后续排查bSocket 空实现，避免 403 
    """
    # 接受 WebSocket 连接，确保握手成功，避免 FastAPI 返回 403
    await websocket.accept()
    # 当前未有具体实时业务需求，因此立即关闭连接，避免占用无效资源
    await websocket.close()
    
@router.get("/favicon.ico", include_in_schema = False)
async def favicon():
    print(os.path.join(dist_dir, "favicon.ico"))
    return FileResponse(os.path.join(dist_dir, "favicon.ico"))

# 新增心跳/检查接口
@router.get("/c_hello")
def c_hello(asker: str = None):
    return {"message": "hello", "asker": asker}
