''' -*- coding: utf-8 -*-
# @Author  : Ficus
# @Time    : 2024/11/2 09:36
# @File    : fastServer.py
'''
import os
import sys
import logging
from typing import Dict, Any

# 设置 COM 线程模型为 STA (单线程单元)，pywinauto 需要此模式
# 必须在导入任何 COM 相关库(如 pythoncom, pywinauto, comtypes)之前设置
sys.coinit_flags = 2

from pydantic import BaseModel
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import mimetypes
import tempfile
import os
import sys
import comtypes.client
import comtypes

# 设置 comtypes 生成目录为临时目录，避免权限问题
try:
    print(f"Original comtypes.client.gen_dir: {comtypes.client.gen_dir}")
    
    comtypes_gen_dir = os.path.join(tempfile.gettempdir(), "comtypes_gen")
    if not os.path.exists(comtypes_gen_dir):
        os.makedirs(comtypes_gen_dir)
        # Ensure it's a package
        init_file = os.path.join(comtypes_gen_dir, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                f.write("")
                
    comtypes.client.gen_dir = comtypes_gen_dir
    print(f"New comtypes.client.gen_dir: {comtypes.client.gen_dir}")
    
    # 关键修改：修改 comtypes.gen 的搜索路径
    import comtypes.gen
    # 将我们的临时目录放在第一位
    if comtypes_gen_dir not in comtypes.gen.__path__:
        comtypes.gen.__path__.insert(0, comtypes_gen_dir)
    print(f"Modified comtypes.gen.__path__: {comtypes.gen.__path__}")
    
except Exception as e:
    print(f"Warning: Failed to set comtypes gen dir: {e}")

# 修复 Windows 下 .js 文件 MIME 类型可能为 text/plain 导致前端无法加载的问题
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/css", ".css")

from router import router_manager
from api import home_router, setting_router, custom_router, autosop_router
# import baseUtil

# 前端文件目录
BASE_DIR = os.path.abspath(os.getcwd())
dist_dir = os.path.join(BASE_DIR, "dist", "gui")
# dist_dir = os.path.join(baseUtil.get_exe_path(), "gui")
static_dir = os.path.join(dist_dir, "assets")

from contextlib import asynccontextmanager
from scheduler import start_scheduler, shutdown_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动定时任务调度器
    start_scheduler()
    yield
    # 关闭定时任务调度器
    shutdown_scheduler()

app = FastAPI(docs_url=None, lifespan=lifespan)

# 注册路由
app.include_router(router_manager.router)
app.include_router(setting_router, prefix="/api/setting", tags=["config"])
app.include_router(home_router, prefix="/api/home", tags=["home"])
app.include_router(custom_router, prefix="/api/custom", tags=["custom"])
app.include_router(autosop_router, prefix="/api/autosop", tags=["autosop"])
app.mount("/assets", StaticFiles(directory=static_dir), name="assets")


class BaseMap(BaseModel):
    data: Dict[str, Any]

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    # API 404
    if full_path.startswith("api/"):
        return Response(status_code=404)
    
    # Try to serve static file
    file_path = os.path.join(dist_dir, full_path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    
    # SPA Fallback
    index_path = os.path.join(dist_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return Response("Index file not found", status_code=404)
