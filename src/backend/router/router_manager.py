''' -*- coding: utf-8 -*-
# @Author  : Ficus
# @Time    : 2024/11/4 15:14
# @File    : server.py
'''
import os

from fastapi import APIRouter, WebSocket, Response, WebSocketDisconnect
from fastapi.responses import FileResponse, HTMLResponse
from loguru import logger
from environment import env, EnvMode
import importlib.util
from config.env import *
from utils.response_util import ResponseUtil

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
    try:
        # 保持连接打开，直到客户端主动断开，避免 Windows 下服务端主动关闭导致 ConnectionResetError
        while True:
            await websocket.receive_text()
    except (WebSocketDisconnect, Exception):
        pass
    
@router.get("/favicon.ico", include_in_schema = False)
async def favicon():
    file_path = os.path.join(dist_dir, "favicon.ico")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return Response(status_code=404)

# 新增心跳/检查接口
@router.get("/api/c_hello")
def c_hello(asker: str = None):
    # 在心跳接口内记录简要调用者信息，原因：便于定位谁在调用健康检查，同时避免敏感信息泄露
    logger.info(f"/api/c_hello called, asker={asker or 'unknown'}")
    return ResponseUtil.success(data={"message": "hello", "asker": asker})
