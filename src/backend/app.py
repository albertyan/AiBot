''' -*- coding: utf-8 -*-
# @Author  : Ficus
# @Time    : 2024/11/2 09:36
# @File    : fastServer.py
'''
import os
import logging
from typing import Dict, Any

from pydantic import BaseModel
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import mimetypes

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

app = FastAPI(docs_url=None)

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
